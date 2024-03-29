from copy import deepcopy
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from caseworker.core.constants import Permission
from core.helpers import convert_dict_to_query_params
from caseworker.core.objects import Tab
from caseworker.core.services import get_user_permissions, get_menu_notifications, get_countries
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.organisations import OrganisationsPage, OrganisationPage
from lite_forms.components import FiltersBar, TextInput, Select, Option, HiddenField
from lite_forms.common import edit_address_questions_form
from lite_forms.helpers import flatten_data
from lite_forms.views import MultiFormView, SingleFormView
from caseworker.organisations.forms import (
    register_organisation_forms,
    register_hmrc_organisation_forms,
    edit_commercial_form,
    edit_individual_form,
    review_organisation_form,
)
from caseworker.organisations.services import (
    get_organisations,
    get_organisation_sites,
    get_organisation,
    post_organisations,
    put_organisation,
    get_organisation_members,
    post_hmrc_organisations,
    put_organisation_status,
    get_organisation_activity,
    get_site_activity,
)

from core.auth.views import LoginRequiredMixin


class OrganisationList(LoginRequiredMixin, TemplateView):
    """
    Show all organisations.
    """

    def get(self, request, **kwargs):
        search_term = request.GET.get("search_term", "").strip()
        org_type = request.GET.get("org_type", "").strip()

        params = {"page": int(request.GET.get("page", 1)), "status": request.GET.get("status", "active")}
        if search_term:
            params["search_term"] = search_term
        if org_type:
            params["org_type"] = org_type

        organisations, _ = get_organisations(request, convert_dict_to_query_params(params))

        filters = FiltersBar(
            [
                TextInput(name="search_term", title=OrganisationsPage.Filters.NAME),
                Select(
                    name="org_type",
                    title=OrganisationsPage.Filters.TYPE,
                    options=[
                        Option("individual", OrganisationsPage.Filters.Types.INDIVIDUAL),
                        Option("commercial", OrganisationsPage.Filters.Types.COMMERCIAL),
                        Option("hmrc", OrganisationsPage.Filters.Types.HMRC),
                    ],
                ),
                HiddenField(name="status", value=params["status"]),
            ]
        )

        context = {
            "data": organisations,
            "filters": filters,
            "search_term": params.get("search_term", ""),
            "tab": params.get("status"),
            "in_review_total": get_menu_notifications(request)["notifications"].get("organisations"),
            "can_manage_organisations": Permission.MANAGE_ORGANISATIONS.value in get_user_permissions(request),
        }
        return render(request, "organisations/index.html", context)


class OrganisationView(TemplateView):
    organisation_id = None
    organisation = None
    additional_context = {}

    def get_additional_context(self):
        return self.additional_context

    def get(self, request, **kwargs):
        self.organisation_id = kwargs["pk"]
        self.organisation = get_organisation(request, self.organisation_id)

        context = {
            "organisation": self.organisation,
            "can_manage_organisations": Permission.MANAGE_ORGANISATIONS.value in get_user_permissions(request),
            "tabs": [
                Tab(
                    "details",
                    OrganisationPage.Details.TITLE,
                    reverse_lazy("organisations:organisation", kwargs={"pk": self.organisation_id}),
                ),
                Tab(
                    "members",
                    OrganisationPage.Members.TITLE,
                    reverse_lazy("organisations:organisation_members", kwargs={"pk": self.organisation_id}),
                ),
                Tab(
                    "sites",
                    OrganisationPage.Sites.TITLE,
                    reverse_lazy("organisations:organisation_sites", kwargs={"pk": self.organisation_id}),
                ),
            ],
            "activity": get_organisation_activity(request, self.organisation_id),
        }
        context.update(self.get_additional_context())
        return render(request, f"organisations/organisation/{self.template_name}.html", context)


class OrganisationDetails(LoginRequiredMixin, OrganisationView):
    template_name = "details"

    def get_additional_context(self):
        context = super().get_additional_context()
        documents = {item["document_type"].replace("-", "_"): item for item in self.organisation["documents"]}
        return {**context, "orgasation_documents": documents}


class OrganisationReview(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.action = put_organisation_status
        self.form = review_organisation_form(request, self.object_pk)
        self.success_url = reverse_lazy("organisations:organisation", kwargs={"pk": self.object_pk})


class OrganisationMembers(LoginRequiredMixin, OrganisationView):
    template_name = "members"

    def get_additional_context(self):
        return {"members": get_organisation_members(self.request, self.organisation_id)}


class OrganisationSites(LoginRequiredMixin, OrganisationView):
    template_name = "sites"

    def get_additional_context(self):
        return {
            "sites": get_organisation_sites(self.request, self.organisation_id),
            "activity": get_site_activity(self.request, self.organisation_id),
        }


class RegisterOrganisation(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = register_organisation_forms(request)
        self.action = post_organisations
        self.success_message = strings.ORGANISATION_CREATION_SUCCESS
        self.success_url = reverse("organisations:organisations")


class RegisterHMRC(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = register_hmrc_organisation_forms()
        self.action = post_hmrc_organisations
        self.success_message = strings.HMRC_ORGANISATION_CREATION_SUCCESS
        self.success_url = reverse("organisations:organisations")


class EditOrganisation(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        organisation = get_organisation(request, str(self.object_pk))
        self.data = organisation
        self.action = put_organisation
        self.success_url = reverse_lazy("organisations:organisation", kwargs={"pk": self.object_pk})

    def get_form(self):
        user_permissions = get_user_permissions(self.request)
        permission_to_edit_org_name = (
            Permission.MANAGE_ORGANISATIONS.value in user_permissions
            and Permission.REOPEN_CLOSED_CASES.value in user_permissions
        )
        if self.data["primary_site"]["address"].get("address_line_1"):
            are_fields_optional = "address" in self.data["primary_site"]["address"].get("address_line_1")
        else:
            are_fields_optional = self.data["primary_site"]["address"]

        form = edit_commercial_form if self.data["type"]["key"] == "commercial" else edit_individual_form

        return form(self.data, permission_to_edit_org_name, are_fields_optional)


class EditOrganisationAddress(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.organisation = get_organisation(request, str(self.object_pk))
        self.data = self.organisation
        self.action = put_organisation
        self.success_url = reverse_lazy("organisations:organisation", kwargs={"pk": self.object_pk})

    def get_data(self):
        data = deepcopy(self.data)
        data["site"] = data.pop("primary_site")
        return {
            **flatten_data(data),
            "site.address.country": self.organisation["primary_site"]["address"]["country"]["id"],
        }

    def get_form(self):
        is_commercial = self.organisation["type"]["key"] == "commercial"
        in_uk = self.organisation["primary_site"]["address"]["country"]["id"] == "GB"
        countries = get_countries(self.request, True, ["GB"])
        return edit_address_questions_form(is_commercial, in_uk, countries, prefix="site.address.")
