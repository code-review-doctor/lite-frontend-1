from django.views.generic import FormView, TemplateView
from django.urls import reverse

from caseworker.advice import forms, services
from caseworker.advice.constants import DECISION_TYPE_VERB_MAPPING

from core import client

from caseworker.cases.services import get_case
from caseworker.core.services import get_denial_reasons
from core.auth.views import LoginRequiredMixin


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    @property
    def case_id(self):
        return str(self.kwargs["pk"])

    @property
    def case(self):
        return get_case(self.request, self.case_id)

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        return {**context, **self.get_context(), "case": self.case, "queue_pk": self.kwargs["queue_pk"]}


class CaseDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    """This endpoint renders case detail panel. This will probably
    not be used stand-alone. This is useful for testing the case
    detail template ATM.
    """

    template_name = "advice/case_detail_example.html"


class SelectAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/select_advice.html"
    form_class = forms.SelectAdviceForm

    def get_success_url(self):
        recommendation = self.request.POST.get("recommendation")
        if recommendation == "approve_all":
            return reverse("cases:approve_all", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
        else:
            return "/#refuse"


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    form_class = forms.GiveApprovalAdviceForm
    template_name = "advice/give-approval-advice.html"

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_approval_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"
    form_class = forms.RefusalAdviceForm

    def get_form_kwargs(self):
        """Overriding this so that I can pass denial_reasons
        to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["denial_reasons"] = get_denial_reasons(self.request)
        return kwargs

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_refusal_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class AdviceDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/view_my_advice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = context["case"]
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        nlr_products = services.filter_nlr_products(case["data"]["goods"])
        return {**context, "my_advice": my_advice, "nlr_products": nlr_products}


class EditAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to edit given advice for all products on the application
    """

    def get_form(self):
        case = get_case(self.request, self.kwargs["pk"])
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        advice = my_advice[0]

        if advice["type"]["key"] in ["approve", "proviso"]:
            self.advice_type = "approve"
            self.template_name = "advice/give-approval-advice.html"
            return forms.get_approval_advice_form_factory(advice)
        elif advice["type"]["key"] == "refuse":
            self.advice_type = "refuse"
            self.template_name = "advice/refusal_advice.html"
            denial_reasons = get_denial_reasons(self.request)
            return forms.get_refusal_advice_form_factory(advice, denial_reasons)
        else:
            raise ValueError("Invalid advice type encountered")

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        data = form.cleaned_data.copy()
        if self.advice_type == "approve":
            for field in form.changed_data:
                data[field] = self.request.POST.get(field)
            services.post_approval_advice(self.request, case, data)
        elif self.advice_type == "refuse":
            data["refusal_reasons"] = self.request.POST.get("refusal_reasons")
            data["denial_reasons"] = self.request.POST.getlist("denial_reasons")
            services.post_refusal_advice(self.request, case, data)
        else:
            raise ValueError("Unknown advice type")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class DeleteAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/delete-advice.html"
    form_class = forms.DeleteAdviceForm

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.delete_user_advice(self.request, case["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class AdviceView(CaseContextMixin, TemplateView):
    template_name = "advice/view-advice.html"

    @property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @property
    def queue(self):
        response = client.get(self.request, f"/queues/{self.queue_id}")
        response.raise_for_status()
        return response.json()

    @property
    def teams(self):
        return {advice["user"]["team"]["id"]: advice["user"]["team"] for advice in self.case["advice"]}.values()

    @property
    def grouped_advice(self):
        if not self.case["advice"]:
            return []

        return self.group_advice()

    def group_user_advice(self, user_advice, destination):
        advice_item = [a for a in user_advice if a[destination["type"]] is not None][0]
        return {
            "type": destination["name"],
            "address": destination["address"],
            "licence_condition": advice_item["proviso"],
            "country": destination["country"]["name"],
            "advice": advice_item,
        }

    def group_user_decision_advice(self, user_advice, team_user, decision):
        return {
            "user": team_user,
            "decision": decision,
            "decision_verb": DECISION_TYPE_VERB_MAPPING[decision],
            "advice": [self.group_user_advice(user_advice, destination) for destination in self.case.destinations],
        }

    def group_team_user_advice(self, team, team_advice, team_user):
        user_advice = [advice for advice in team_advice if advice["user"]["id"] == team_user["id"]]
        decisions = set([advice["type"]["value"] for advice in user_advice])
        return {
            "team": team,
            "advice": [self.group_user_decision_advice(user_advice, team_user, decision) for decision in decisions],
        }

    def group_advice(self):
        grouped_advice = []

        for team in self.teams:
            team_advice = [advice for advice in self.case["advice"] if advice["user"]["team"]["id"] == team["id"]]
            team_users = {
                advice["user"]["id"]: advice["user"]
                for advice in self.case["advice"]
                if advice["user"]["team"]["id"] == team["id"]
            }.values()
            grouped_advice += [self.group_team_user_advice(team, team_advice, team_user) for team_user in team_users]

        return grouped_advice

    def get_context(self):
        return {
            "queue": self.queue,
            "grouped_advice": self.grouped_advice,
        }
