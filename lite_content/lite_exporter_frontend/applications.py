class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"


class EndUserForm:
    TITLE = "Select the type of end user"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserForm:
    TITLE = "Select the type of ultimate recipient"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneeForm:
    TITLE = "Select the type of consignee"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class ThirdPartyForm:
    class Options:
        AGENT = "Agent or broker"
        ADDITIONAL_END_USER = "End user"
        INTERMEDIATE_CONSIGNEE = "Intermediate consignee"
        SUBMITTER = "Authorised submitter"
        CONSULTANT = "Consultant"
        CONTACT = "Contact"
        EXPORTER = "Exporter"

    TITLE = "Select the type of third party"
    BUTTON = "Save and continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class GeneratedDocuments:
    TAB = "ECJU Documents"
    NO_DOCUMENTS = "There are currently no documents from ECJU."

    class Table:
        NAME_COLUMN = "Name"
        DATE_COLUMN = "Date"
        DOWNLOAD_LINK = "Download"


class ApplicationSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created at"
    SUBMITTED_AT = "Submitted at"
    END_USER = "End user"
    ULTIMATE_END_USERS = "Ultimate recipient"
    CONSIGNEE = "Consignee"
    THIRD_PARTIES = "Third parties"
    GOODS_LOCATIONS = "Product locations"
    SUPPORTING_DOCUMENTATION = "Supporting documentation"
    GOODS = "Products"
    COUNTRIES = "Countries"
    ON_BEHALF_OF = "On behalf of"
    OPTIONAL_NOTE = "Optional note"


class ApplicationsSummaryPage:
    REFERENCE_NAME = "Reference"
    TYPE = "Licence type"
    EXPORT_TYPE = "Export type"
    STATUS = "Status"
    LAST_UPDATED_AT = "Last updated"
    CREATED_AT = "Created at"
    SUBMITTED_AT = "Submitted at"


class InitialApplicationQuestionsForms:
    WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE = "Select the type of licence you need"
    WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION = ""
    STANDARD_LICENCE = "Standard licence"
    STANDARD_LICENCE_DESCRIPTION = "Select a standard licence for a set quantity and set value of products."
    OPEN_LICENCE = "Open licence"
    OPEN_LICENCE_DESCRIPTION = (
        "Select an open licence for multiple shipments of specific products to specific countries. "
        "Open licences cover long term projects and repeat business."
    )
    HELP_WITH_CHOOSING_A_LICENCE = "Help with choosing a licence"
    HELP_WITH_CHOOSING_A_LICENCE_CONTENT = (
        "If you're unsure about which licence to select, read the guidance on "
        'GOV.UK for <a class="govuk-link" target="_blank" '
        'href="https://www.gov.uk/starting-to-export/licences">exporting and doing business '
        'abroad<span class="govuk-visually-hidden"> (opens in a new window or tab)</span></a>.'
    )
    ENTER_A_REFERENCE_NAME_TITLE = "Application reference"
    ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
    ENTER_A_REFERENCE_NAME_DESCRIPTION = "Name and save this application so you can refer back to it when needed."
    TEMPORARY_OR_PERMANENT_TITLE = "Select an export type"
    TEMPORARY_OR_PERMANENT_DESCRIPTION = ""
    TEMPORARY = "Temporary"
    PERMANENT = "Permanent"
    HAVE_YOU_BEEN_INFORMED_TITLE = (
        "Have you been informed under an end use control that you need to apply for a licence?"
    )
    HAVE_YOU_BEEN_INFORMED_DESCRIPTION = "This could be a letter or email from HMRC or another government department."
    WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number (optional)"
    WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "The reference number is on the letter or email."


class DestinationForm:
    TITLE = "Where are your products going?"
    DESCRIPTION = "Select all countries that apply."
