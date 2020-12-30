from django.urls import reverse_lazy

from caseworker.cases.services import get_case_types, get_flags_for_team_of_level
from caseworker.core.services import get_statuses, get_countries
from lite_content.lite_internal_frontend.routing_rules import (
    AdditionalRules,
    DeactivateForm,
    ActivateForm,
    Forms,
)
from lite_forms.components import (
    FormGroup,
    Form,
    Label,
    Select,
    AutocompleteInput,
    TextInput,
    Checkboxes,
    Option,
    RadioButtons,
    BackLink,
    HiddenField,
    HTMLBlock,
    Filter,
    Button,
)
from lite_forms.generators import confirm_form
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle
from caseworker.teams.services import get_users_by_team, get_teams, get_team_queues

additional_rules = [
    Option("case_types", AdditionalRules.CASE_TYPES),
    Option("flags", AdditionalRules.FLAGS),
    Option("country", AdditionalRules.COUNTRY),
    Option("users", AdditionalRules.USERS),
]


def select_a_team(request):
    return Form(
        title=Forms.TEAM,
        questions=[RadioButtons(name="team", options=get_teams(request, True)),],
        back_link=BackLink(Forms.BACK_BUTTON, reverse_lazy("routing_rules:list")),
    )


def initial_routing_rule_questions(request, select_team, team_id, is_editing: bool):
    select_team_question = []
    if select_team:
        select_team_question = [
            AutocompleteInput(
                title=Forms.TEAM,
                name="team",
                options=get_teams(request, True),
                description="Type to get suggestions. For example, TAU.",
            ),
        ]

    return Form(
        title=Forms.EDIT_TITLE if is_editing else Forms.CREATE_TITLE,
        questions=select_team_question
        + [
            Select(title=Forms.CASE_STATUS, name="status", options=get_statuses(request, True)),
            AutocompleteInput(
                title=Forms.QUEUE,
                name="queue",
                options=get_team_queues(request, team_id, True, True) if team_id else [],
                description="Type to get suggestions.\nFor example, HMRC enquiries.",
            ),
            TextInput(title=Forms.TIER, name="tier"),
            HiddenField(name="additional_rules[]", value=None),
            Checkboxes(title=Forms.ADDITIONAL_RULES, name="additional_rules[]", options=additional_rules,),
        ],
        back_link=BackLink(Forms.BACK_BUTTON, reverse_lazy("routing_rules:list")),
    )


def select_case_type(request):
    return Form(
        title=Forms.CASE_TYPES,
        questions=[
            Checkboxes(
                name="case_types[]",
                options=[
                    Option(option["id"], option["reference"]["value"]) for option in get_case_types(request, False)
                ],
            )
        ],
    )


def get_flag_details_html(flag):
    rules_html = ""
    rules = flag["flagging_rules"]
    if rules:
        rows = []
        for rule in rules:
            group_entries = [f"{g} group" for g in rule["matching_groups"]]
            all_entries = ", ".join(rule["matching_values"] + group_entries)
            rows.append(
                f"""
                <div class="govuk-summary-list__row govuk-summary-list__row--no-border">
                    <dt class="govuk-summary-list__key govuk-!-padding-top-0">Parameter:</dt>
                    <dd class="govuk-summary-list__value govuk-!-padding-top-0 govuk-!-width-two-thirds">{rule["level"]}</dd>
                </div>
                <div class="govuk-summary-list__row govuk-summary-list__row--no-border">
                    <dt class="govuk-summary-list__key govuk-!-padding-top-0">In</dt>
                    <dd class="govuk-summary-list__value govuk-!-padding-top-0 govuk-!-width-two-thirds">{all_entries}</dd>
                </div>
            """
            )
        rules_html = "<hr>".join(rows)
    else:
        rules_html = "None"

    return f"""
        <li>{flag["name"]}</li>
        <details class="govuk-details" data-module="govuk-details">
            <summary class="govuk-details__summary">
                <span class="govuk-details__summary-text">
                Flagging rules
                </span>
            </summary>
            <div class="govuk-details__text">
                <dl class="govuk-summary-list">
                    {rules_html}
                </dl>
            </div>
        </details>
    """


def select_flags(request, team_id, flags_to_include, flags_to_exclude):
    return Form(
        title=Forms.FLAGS,
        questions=[
            HiddenField(name="flags_to_include", value=",".join(flags_to_include)),
            HiddenField(name="flags_to_exclude", value=",".join(flags_to_exclude)),
            HTMLBlock("<div id='routing-rules-flags-details'></div>"),
            Filter(),
            Checkboxes(
                name="flags[]",
                options=[
                    Option(flag["id"], flag["name"], data_attribute=get_flag_details_html(flag))
                    for flag in get_flags_for_team_of_level(
                        request, level="", team_id=team_id, include_system_flags=True
                    )[0]
                ],
                import_custom_js=["/javascripts/filter-checkbox-list-flags.js"],
            ),
            Label(text="Apply routing rules to cases that"),
            RadioButtons(
                title="",
                name="routing_rules_flags_condition",
                options=[
                    Option(key="contain_selected_flags", value="Contain selected flags"),
                    Option(key="doesnot_contain_selected_flags", value="Do not contain selected flags"),
                ],
            ),
        ],
        buttons=[
            Button("Save and continue", "submit"),
            Button("Add another condition", "", ButtonStyle.SECONDARY, link="#"),
        ],
        javascript_imports={"/javascripts/routing-rules-flags.js"},
    )


def select_country(request):
    return Form(
        title=Forms.COUNTRY,
        questions=[AutocompleteInput(name="country", options=get_countries(request, convert_to_options=True),)],
    )


def select_team_member(request, team_id):
    return Form(
        title=Forms.USER,
        questions=[
            RadioButtons(
                name="user", options=get_users_by_team(request, team_id, convert_to_options=True) if team_id else [],
            )
        ],
    )


def routing_rule_form_group(
    request, additional_rules, team_id, flags_to_include, flags_to_exclude, is_editing=False, select_team=False
):
    return FormGroup(
        [
            initial_routing_rule_questions(request, select_team, team_id, is_editing),
            conditional("case_types" in additional_rules, select_case_type(request)),
            conditional(
                "flags" in additional_rules, select_flags(request, team_id, flags_to_include, flags_to_exclude)
            ),
            conditional("country" in additional_rules, select_country(request)),
            conditional("users" in additional_rules, select_team_member(request, team_id)),
        ]
    )


def deactivate_or_activate_routing_rule_form(activate, status):
    if activate:
        title = ActivateForm.TITLE
        description = ActivateForm.DESCRIPTION
        yes_label = ActivateForm.YES_LABEL
        no_label = ActivateForm.NO_LABEL
    else:
        title = DeactivateForm.TITLE
        description = DeactivateForm.DESCRIPTION
        yes_label = DeactivateForm.YES_LABEL
        no_label = DeactivateForm.NO_LABEL

    return confirm_form(
        title=title,
        description=description,
        back_link_text=Forms.BACK_BUTTON,
        back_url=reverse_lazy("routing_rules:list"),
        yes_label=yes_label,
        no_label=no_label,
        hidden_field=status,
        confirmation_name="confirm",
    )
