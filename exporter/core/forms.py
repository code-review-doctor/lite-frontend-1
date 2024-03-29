from exporter.core.helpers import str_date_only
from exporter.core.services import get_countries
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.core import StartPage, RegisterAnOrganisation
from lite_forms.common import address_questions, foreign_address_questions
from lite_forms.components import (
    RadioButtons,
    Option,
    Form,
    FormGroup,
    TextInput,
    Breadcrumbs,
    BackLink,
    Label,
    List,
    HiddenField,
)
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle


def select_your_organisation_form(organisations):
    return Form(
        "Select an organisation",
        "You can switch between organisations from your dashboard.",
        [
            RadioButtons(
                name="organisation",
                options=[
                    Option(x["id"], x["name"], "Member since " + str_date_only(x["joined_at"])) for x in organisations
                ],
            )
        ],
        default_button_name="Save and continue",
        back_link=None,
    )


def register_triage():
    from exporter.core.views import RegisterAnOrganisationTriage

    return FormGroup(
        [
            Form(
                title=RegisterAnOrganisation.Landing.TITLE,
                questions=[
                    Label(RegisterAnOrganisation.Landing.DESCRIPTION),
                    Label(RegisterAnOrganisation.Landing.DESCRIPTION_2),
                    Label(RegisterAnOrganisation.Landing.SUMMARY_LIST_HEADER),
                    List(StartPage.BULLET_POINTS, type=List.ListType.BULLETED),
                    Label(StartPage.NOTICE, classes=["govuk-inset-text"]),
                ],
                default_button_name=RegisterAnOrganisation.Landing.BUTTON,
                default_button_style=ButtonStyle.START,
                back_link=Breadcrumbs([*[BackLink(x[0], x[1]) for x in StartPage.BREADCRUMBS], BackLink("LITE", None)]),
            ),
            Form(
                title=RegisterAnOrganisation.CommercialOrIndividual.TITLE,
                description=RegisterAnOrganisation.CommercialOrIndividual.DESCRIPTION,
                caption="Step 1 of 4",
                questions=[
                    RadioButtons(
                        name="type",
                        options=[
                            Option(
                                key="commercial",
                                value=RegisterAnOrganisation.CommercialOrIndividual.COMMERCIAL,
                                description=RegisterAnOrganisation.CommercialOrIndividual.COMMERCIAL_DESCRIPTION,
                            ),
                            Option(
                                key="individual",
                                value=RegisterAnOrganisation.CommercialOrIndividual.INDIVIDUAL,
                                description=RegisterAnOrganisation.CommercialOrIndividual.INDIVIDUAL_DESCRIPTION,
                            ),
                        ],
                    )
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title=RegisterAnOrganisation.WhereIsYourOrganisationBased.TITLE,
                description=RegisterAnOrganisation.WhereIsYourOrganisationBased.DESCRIPTION,
                caption="Step 2 of 4",
                questions=[
                    RadioButtons(
                        name="location",
                        options=[
                            Option(
                                key=RegisterAnOrganisationTriage.Locations.UNITED_KINGDOM,
                                value=RegisterAnOrganisation.WhereIsYourOrganisationBased.IN_THE_UK,
                                description=RegisterAnOrganisation.WhereIsYourOrganisationBased.IN_THE_UK_DESCRIPTION,
                            ),
                            Option(
                                key=RegisterAnOrganisationTriage.Locations.ABROAD,
                                value=RegisterAnOrganisation.WhereIsYourOrganisationBased.OUTSIDE_THE_UK,
                                description=RegisterAnOrganisation.WhereIsYourOrganisationBased.OUTSIDE_THE_UK_DESCRIPTION,
                            ),
                        ],
                    )
                ],
                default_button_name=generic.CONTINUE,
            ),
        ]
    )


def site_form(request, is_individual, location):
    from exporter.core.views import RegisterAnOrganisationTriage

    is_in_uk = location == RegisterAnOrganisationTriage.Locations.UNITED_KINGDOM

    return Form(
        title=conditional(
            not is_individual,
            conditional(
                is_in_uk,
                RegisterAnOrganisation.Headquarters.TITLE,
                RegisterAnOrganisation.Headquarters.TITLE_FOREIGN,
            ),
            conditional(
                is_in_uk,
                RegisterAnOrganisation.Headquarters.TITLE_INDIVIDUAL,
                RegisterAnOrganisation.Headquarters.TITLE_INDIVIDUAL_FOREIGN,
            ),
        ),
        description=RegisterAnOrganisation.Headquarters.DESCRIPTION,
        caption="Step 4 of 4",
        questions=[
            TextInput(
                title=RegisterAnOrganisation.Headquarters.NAME,
                description=RegisterAnOrganisation.Headquarters.NAME_DESCRIPTION,
                name="site.name",
            ),
            *conditional(
                is_in_uk,
                address_questions(None, is_individual, "site.address."),
                foreign_address_questions(is_individual, get_countries(request, True, ["GB"]), "site.address."),
            ),
        ],
        default_button_name=generic.CONTINUE,
    )


def register_a_commercial_organisation_group(request, location):
    from exporter.core.views import RegisterAnOrganisationTriage

    is_in_uk = location == RegisterAnOrganisationTriage.Locations.UNITED_KINGDOM

    return FormGroup(
        [
            Form(
                title=RegisterAnOrganisation.Commercial.TITLE,
                description=RegisterAnOrganisation.Commercial.DESCRIPTION,
                caption="Step 3 of 4",
                questions=[
                    HiddenField("location", location),
                    TextInput(
                        title=RegisterAnOrganisation.Commercial.NAME,
                        description=RegisterAnOrganisation.Commercial.NAME_DESCRIPTION,
                        name="name",
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Commercial.EORI_NUMBER,
                        description=RegisterAnOrganisation.Commercial.EORI_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Commercial.EORI_NUMBER_SHORT_TITLE,
                        name="eori_number",
                        optional=not is_in_uk,
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Commercial.SIC_NUMBER,
                        description=RegisterAnOrganisation.Commercial.SIC_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Commercial.SIC_NUMBER_SHORT_TITLE,
                        name="sic_number",
                        optional=not is_in_uk,
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Commercial.VAT_NUMBER,
                        description=RegisterAnOrganisation.Commercial.VAT_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Commercial.VAT_NUMBER_SHORT_TITLE,
                        name="vat_number",
                        optional=not is_in_uk,
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Commercial.CRN_NUMBER,
                        description=RegisterAnOrganisation.Commercial.CRN_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Commercial.CRN_NUMBER_SHORT_TITLE,
                        name="registration_number",
                        optional=not is_in_uk,
                    ),
                ],
                default_button_name=generic.CONTINUE,
            ),
            site_form(request, False, location),
        ]
    )


def register_an_individual_group(request, location):
    from exporter.core.views import RegisterAnOrganisationTriage

    is_in_uk = location == RegisterAnOrganisationTriage.Locations.UNITED_KINGDOM

    return FormGroup(
        [
            Form(
                title=RegisterAnOrganisation.Individual.TITLE,
                description=RegisterAnOrganisation.Individual.DESCRIPTION,
                caption="Step 3 of 4",
                questions=[
                    HiddenField("location", location),
                    TextInput(
                        title=RegisterAnOrganisation.Individual.NAME,
                        description=RegisterAnOrganisation.Individual.NAME_DESCRIPTION,
                        name="name",
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Individual.EORI_NUMBER,
                        description=RegisterAnOrganisation.Individual.EORI_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Individual.EORI_NUMBER_SHORT_TITLE,
                        name="eori_number",
                        optional=not is_in_uk,
                    ),
                    TextInput(
                        title=RegisterAnOrganisation.Individual.VAT_NUMBER,
                        description=RegisterAnOrganisation.Individual.VAT_NUMBER_DESCRIPTION,
                        short_title=RegisterAnOrganisation.Individual.VAT_NUMBER_SHORT_TITLE,
                        optional=True,
                        name="vat_number",
                    ),
                ],
                default_button_name=generic.CONTINUE,
            ),
            site_form(request, True, location),
        ]
    )
