import datetime

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView

from caseworker.advice.services import get_advice_tab_context
from caseworker.cases.constants import CaseStatusEnum
from caseworker.cases.helpers.ecju_queries import get_ecju_queries
from caseworker.cases.objects import Slice, Case
from caseworker.cases.services import (
    get_case,
    get_user_case_queues,
    get_case_documents,
    get_case_additional_contacts,
    get_activity,
    get_activity_filters,
)
from caseworker.core.constants import GENERATED_DOCUMENT
from caseworker.core.helpers import generate_activity_filters
from caseworker.core.objects import Tab, TabCollection
from caseworker.core.services import get_user_permissions, get_status_properties, get_permissible_statuses
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasePage, ApplicationPage
from caseworker.queues.services import get_queue
from caseworker.users.services import get_gov_user


class Tabs:
    DETAILS = Tab("details", CasePage.Tabs.DETAILS, "details")
    DOCUMENTS = Tab("documents", CasePage.Tabs.DOCUMENTS, "documents")
    LICENCES = Tab("licences", CasePage.Tabs.LICENCES, "licences")
    ADDITIONAL_CONTACTS = Tab("additional-contacts", CasePage.Tabs.ADDITIONAL_CONTACTS, "additional-contacts")
    ECJU_QUERIES = Tab("ecju-queries", CasePage.Tabs.ECJU_QUERIES, "ecju-queries")
    ACTIVITY = Tab("activity", CasePage.Tabs.CASE_NOTES_AND_TIMELINE, "activity")
    ADVICE = TabCollection(
        "advice",
        "Recommendations and decision",
        children=[
            Tab("user-advice", CasePage.Tabs.USER_ADVICE, "user-advice"),
            Tab("team-advice", CasePage.Tabs.TEAM_ADVICE, "team-advice"),
            Tab("final-advice", CasePage.Tabs.FINAL_ADVICE, "final-advice"),
        ],
    )
    COMPLIANCE_LICENCES = Tab("compliance-licences", CasePage.Tabs.LICENCES, "compliance-licences")


class Slices:
    SUMMARY = Slice("summary")
    GOODS = Slice("goods")
    DESTINATIONS = Slice("destinations")
    SANCTION_MATCHES = Slice("sanctions")
    DENIAL_MATCHES = Slice("denial-matches")
    DELETED_ENTITIES = Slice("deleted-entities")
    LOCATIONS = Slice("locations")
    F680_DETAILS = Slice("f680-details", "F680 details")
    EXHIBITION_DETAILS = Slice("exhibition-details", "Exhibition details")
    END_USE_DETAILS = Slice("end-use-details", "End use details")
    ROUTE_OF_GOODS = Slice("route-of-goods", "Route of goods")
    SUPPORTING_DOCUMENTS = Slice("supporting-documents", "Supporting documents")
    GOODS_QUERY = Slice("goods-query", "Query details")
    GOODS_QUERY_RESPONSE = Slice("goods-query-response")
    HMRC_NOTE = Slice("hmrc-note", "HMRC note")
    END_USER_DETAILS = Slice("end-user-details", "End user details")
    TEMPORARY_EXPORT_DETAILS = Slice("temporary-export-details", "Temporary export details")
    OPEN_APP_PARTIES = Slice("open-app-parties")
    OPEN_GENERAL_LICENCE = Slice("open-general-licence")
    COMPLIANCE_LICENCES = Slice("compliance-licences")
    OPEN_LICENCE_RETURNS = Slice("open-licence-returns", cases.OpenLicenceReturns.TITLE)
    COMPLIANCE_VISITS = Slice("compliance-visits", "Visit reports")
    COMPLIANCE_VISIT_DETAILS = Slice("compliance-visit-details")
    FREEDOM_OF_INFORMATION = Slice("freedom-of-information", "Freedom of Information")


class CaseView(TemplateView):
    case_id = None
    case: Case = None
    queue_id = None
    queue = None
    permissions = None
    tabs = None
    slices = None
    additional_context = {}

    def get_context(self):
        if not self.tabs:
            self.tabs = []
        if not self.slices:
            self.slices = []
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(self.request, self.case_id)
        user_assigned_queues = get_user_case_queues(self.request, self.case_id)[0]
        status_props, _ = get_status_properties(self.request, self.case.data["status"]["key"])
        can_set_done = (
            not status_props["is_terminal"] and self.case.data["status"]["key"] != CaseStatusEnum.APPLICANT_EDITING
        )
        future_next_review_date = (
            True
            if self.case.next_review_date
            and datetime.datetime.strptime(self.case.next_review_date, "%Y-%m-%d").date() > timezone.localtime().date()
            else False
        )
        return {
            "tabs": self.tabs if self.tabs else self.get_tabs(),
            "current_tab": self.kwargs["tab"],
            "slices": [Slices.SUMMARY, *self.slices],
            "case": self.case,
            "queue": self.queue,
            "is_system_queue": self.queue["is_system_queue"],
            "user_assigned_queues": user_assigned_queues,
            "case_documents": get_case_documents(self.request, self.case_id)[0]["documents"],
            "open_ecju_queries": open_ecju_queries,
            "closed_ecju_queries": closed_ecju_queries,
            "additional_contacts": get_case_additional_contacts(self.request, self.case_id),
            "activity": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
            "permissions": self.permissions,
            "can_set_done": can_set_done
            and (self.queue["is_system_queue"] and user_assigned_queues)
            or not self.queue["is_system_queue"],
            "generated_document_key": GENERATED_DOCUMENT,
            "permissible_statuses": get_permissible_statuses(self.request, self.case),
            "filters": generate_activity_filters(get_activity_filters(self.request, self.case_id), ApplicationPage),
            "is_terminal": status_props["is_terminal"],
            "is_read_only": status_props["is_read_only"],
            "has_future_next_review_date": future_next_review_date,
            **self.additional_context,
        }

    def get(self, request, **kwargs):
        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)

        self.permissions = get_user_permissions(self.request)

        if hasattr(self, "get_" + self.case.sub_type + "_" + self.case.type):
            getattr(self, "get_" + self.case.sub_type + "_" + self.case.type)()
        else:
            getattr(self, "get_" + self.case.sub_type)()
        return render(request, "case/case.html", self.get_context())

    def get_tabs(self):
        activity_tab = Tabs.ACTIVITY
        activity_tab.count = "!" if self.case["audit_notification"] else None

        tabs = [
            Tabs.DETAILS,
            Tabs.ADDITIONAL_CONTACTS,
            Tabs.ECJU_QUERIES,
            Tabs.DOCUMENTS,
            activity_tab,
        ]

        return tabs

    def get_advice_tab(self):
        data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))
        return Tab(
            "advice",
            "Recommendations and decision",
            get_advice_tab_context(self.case, data["user"], str(self.kwargs["queue_pk"]))["url"],
            has_template=False,
        )
