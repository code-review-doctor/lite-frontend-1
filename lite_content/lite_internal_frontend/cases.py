class CasesListPage:
    GO_TO_QUEUE = "Go to queue"
    NO_CASES = "There are no new cases to show"
    ACTIVE_FILTER_NO_CASES = "There are no cases to show with those filters"
    EXPORTER_AMENDMENTS_BANNER = "See what cases have changed"
    ASSIGN_USERS = "Assign users"
    STATUS = "Status"

    class Filters:
        CASE_TYPE = "type"
        CASE_STATUS = "status"
        CASE_OFFICER = "case officer"
        ASSIGNED_USER = "assigned user"
        NOT_ASSIGNED = "Not assigned"


class CaseDocumentsPage:
    BACK_LINK = "Back to Case"
    ATTACH = "Attach Document"
    GENERATE = "Generate Document"


class ApplicationPage:
    class Actions:
        CASE_OFFICER = "Assign Case Officer"
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        MOVE = "Move Case"
        CHANGE_STATUS = "Change Status"
        DECISION = "Record Decision"
        ADVICE = "View Advice"
        GENERATE_DOCUMENT = "Generate Document"

    class Goods:
        MISSING_DOCUMENT_REASON_PREFIX = "No document given: "
        TITLE = "Products"

        class Table:
            CLC = "Control List Entry"
            DESCRIPTION = "Description"
            VALUE = "Quantity/Value"
            DOCUMENTS = "Documents"
            FLAGS = "Flags"
            ADVICE = "Advice"

    class Destinations:
        COUNTRY_NAME = "Country"
        PRODUCTS_CONTROL_CODES = "Goods"
        FLAGS_TABLE_HEADER = "Flags"

    class Parties:
        SELECT_ALL = "Select all/Deselect all"
        NAME = "Name"
        ADDRESS = "Address"
        TYPE = "Type"
        WEBSITE = "Website"
        DOCUMENT = "Document"

    class EndUser:
        NO_END_USER = "The applicant is editing the end user."

        class Table:
            Title = "End user"

    class Consignee:
        NO_CONSIGNEE = "The applicant is editing the consignee."

        class Table:
            Title = "Consignee"

    class ThirdParty:
        ROLE = "Role: "

    EDIT_FLAGS = "Edit products flags"
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    REVIEW_GOODS = "Review Products"
    ADVICE = "Give or change advice"
    RESPOND_BUTTON = "Respond to Query"
    CLOSED = "This case is closed"
    CASE_OFFICER = "Case Officer: "
    NO_CASE_OFFICER = "No Case Officer set."


class FinalisePage:
    class Duration:
        TITLE = "Duration"
        DESCRIPTION = "This must be a whole number of months, such as 12"

    class Date:
        TITLE = "Start Date"
        DESCRIPTION = "For example, 27 3 2007"

    class BackLink:
        GOODS_AND_COUNTRIES = "Back to finalise goods and countries"
        FINAL_ADVICE = "Back to final advice"


class GenerateDocumentsPage:
    TITLE = "Generate Document"
    ERROR = "Document Generation is unavailable at this time"

    class SelectTemplateForm:
        BACK_LINK = "Back to Case Documents"

    class EditTextForm:
        HEADING = "Edit text"
        BACK_LINK = "Back to Templates"
        BACK_LINK_REGENERATE = "Back to Case Documents"
        ADD_PARAGRAPHS_LINK = "Add paragraphs"
        BUTTON = "Continue"

    class AddParagraphsForm:
        HEADING = "Add paragraphs"
        BUTTON = "Continue"


class AdditionalDocumentsPage:
    class Table:
        NAME_COLUMN = "Name"
        DOCUMENT_TYPE_COLUMN = "Type"
        DESCRIPTION_COLUMN = "Description"
        USER_COLUMN = "Added by"
        DATE_COLUMN = "Date"

    class Document:
        DOWNLOAD_LINK = "Download"
        INFECTED_LABEL = "Infected"
        PROCESSING_LABEL = "Processing"
        REGENERATE_LINK = "Regenerate"


class EndUserAdvisoriesPage:
    class Actions:
        CASE_OFFICER = "Assign Case Officer"
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        ECJU = "ECJU Queries"
        GENERATE_DOCUMENT = "Generate Document"
        MOVE = "Move Case"

    class Details:
        TITLE = "End User Details"
        NAME = "Name"
        TYPE = "Type"
        EMAIL = "Email"
        TELEPHONE = "Telephone"
        NATURE_OF_BUSINESS = "Nature of Business"
        PRIMARY_CONTACT_NAME = "Primary contact name"
        PRIMARY_CONTACT_JOB = "Primary contact job title"
        PRIMARY_CONTACT_EMAIL = "Primary contact email"
        PRIMARY_CONTACT_TELEPHONE = "Primary contact telephone"
        ADDRESS = "Address"
        WEBSITE = "Website"
        REASONING = "Reasoning behind query"
        NOTES = "Notes about end user"
        COPY_FROM = "Copied From"

    CASE_OFFICER = "Case Officer: "
    EDIT_DESTINATION_FLAGS = "Edit destination flags"
    NO_CASE_OFFICER = "No Case Officer set."


class HMRCPage:
    class Heading:
        EXPORTER = "Exporter "
        RAISED_BY = "Raised by "

    class Actions:
        CHANGE_STATUS = "Change Status"
        DOCUMENT = "Attached Documents"
        MOVE = "Move Case"
        RECORD_DECISION = "Record Decision"
        GENERATE_DOCUMENT = "Generate Document"

    class DenialReasons:
        TITLE = "Denial Reasons"
        REASON = "This case was denied because"
        FURTHER_INFO = "Further information"

    class Good:
        REVIEW_GOODS = "Review products"
        EDIT_FLAGS = "Set flags"
        DESCRIPTION = "Description"
        CONTROL_CODE = "Control list entry"
        CONTROLLED = "Controlled"
        FLAGS = "Flags"

    class SupportingDocumentation:
        TITLE = "Supporting Documentation"
        NAME = "Name"
        DESCRIPTION = "Description"
        DOCUMENT = "Document"

    CASE_FLAGS = "All Flags"


class CaseOfficerPage:
    ERROR = "There is a problem"

    class CurrentOfficer:
        TITLE = "Current case officer"
        FULLNAME = "Name"
        TEAM = "Team"
        EMAIL = "Email"
        REMOVE = "Unassign"
        BUTTON = "Unassign"

    class Error:
        GENERIC = "There appears to be a problem"
        NO_SELECTION = "Please select a user to assign"

    class Search:
        TITLE = "Assign a case officer"
        DESCRIPTION = "A case officer oversees the case for its lifespan."
        PLACEHOLDER = "Search users"
        SEARCH = "Search"
        ASSIGN = "Assign user as case officer"
        NO_RESULTS = "No users matching the criteria"


class StandardApplication:
    LICENSEE = "Licensee"
    END_USER = "End user"
    CONSIGNEE = "Consignee"
    ULTIMATE_END_USER = "Ultimate end user"
    THIRD_PARTY = "Third party"


class OpenApplication:
    SET_FLAGS = "Set flags"
    REVIEW_PRODUCTS = "Review products"


class ClcQuery:
    class Verified:
        OUTCOME = "Outcome"
        CONTROLLED = "Is the good controlled?"
        CONTROL_CODE = "What's the goods actual control list entry"
        REPORT = "Report Summary (optional)"
        COMMENT = "Why was this outcome chosen"

    class GoodDetails:
        TITLE = "Good Details"
        DESCRIPTION = "Description"
        CONTROLLED = "Controlled"
        CONTROL_CODE = "Control list entry"
        EXPECTED_CONTROL_CODE = "Expected Control list entry"
        REASON = "Reason"
        PART_NUMBER = "Part Number"
        FLAGS = "Flags"
        QUERY_TEXT = "CLC query Text"

    class Documents:
        TITLE = "Documents"
        DOWNLOAD = "Download"


class ChangeStatusPage:
    TITLE_APPLICATION = "Application Status"
    TITLE_CLC = "CLC Query Status"
    TITLE_EUA = "End User Advisory Status"


class ReviewGoodsSummary:
    BACK_LINK = "Back to case"
    HEADING = "Review Goods"
    REVIEW_BUTTON = "Review and confirm item"
    SET_FLAGS = "Set goods flags"

    class Table:
        DESCRIPTION = "Description"
        REPORT_SUMMARY = "Report summary"
        CONTROLLED = "Controlled"
        CONTROL_LIST_ENTRY = "Control list entry"
        GOODS_COMMENT = "Goods comment"
        FLAGS = "Flags"
        QUANTITY_VALUE = "Quantity/Value"

    class NotSet:
        REPORT_SUMMARY = "Not Set"
        COMMENT = "Not Set"
        FLAGS = "None Set"


class EcjuQueries:
    BACK_TO_CASE = "Back to Case"
    CASE_HAS_NO_QUERIES = "This case has no ECJU Queries"
    CLOSED = "Closed queries"
    OPEN = "Open queries"
    TITLE = "ECJU Queries"

    class AddQuery:
        ADD_BUTTON_LABEL = "Add an ECJU Query"
        DESCRIPTION = (
            "Enter a full description. If your question is related to goods, then include technical"
            " details if appropriate."
        )
        DROPDOWN_DESCRIPTION = (
            "You can:<ul><li>write a new question, or</li><li>choose a question from a list</li></ul>"
        )
        DROPDOWN_TITLE = "Ask a question"
        TITLE = "Write or edit your question"


class Advice:
    ERROR = "There is a problem"
    IMPORT_ADVICE = "Import advice from picklists"
    IMPORT_PROVISO = "Import proviso from picklists"
    OTHER = "Is there anything else you want to say to the applicant? (optional)"
    REASON = "What are your reasons for this decision?"
    TEXT_ON_LICENCE = "This will appear on the generated documentation"


class Manage:
    class Documents:
        CASE_HAS_NO_DOCUMENTS = "This case has no documents"
        DESCRIPTION = "These are all the documents that have been uploaded to this case."
        DOWNLOAD_DOCUMENT = "Download document"
        PROCESSING = "Processing"
        VIRUS_INFECTED = "Virus infected"
        TITLE = "Case Documents"

        class AttachDocuments:
            BACK_TO_CASE_DOCUMENTS = "Back to Case Documents"
            BUTTON = "Attach Document"
            DESCRIPTION = "Maximum size: 100MB per file"
            DESCRIPTION_FIELD_DETAILS = "optional"
            DESCRIPTION_FIELD_TITLE = "Document description"
            FILE_TOO_LARGE = "The file you tried to upload was too large."
            TITLE = "Attach a document to this case"

    class MoveCase:
        BUTTON = "Move Case"
        DESCRIPTION = "Select all queues that apply."
        TITLE = "Where do you want to move this case?"

    class AssignUsers:
        DESCRIPTION = "Select all users that apply."
        MULTIPLE_TITLE = "Which users do you want to assign to these cases?"
        MULTIPLE_WARNING = "Users already assigned to these cases will be overwritten."
        TITLE = "Which users do you want to assign to this case?"


class Tabs:
    class Activity:
        CHARACTER_LIMIT_2200 = "You can enter up to 2200 characters"
        CANCEL_POST = "Cancel"
        POST = "Post note"


class ReviewGoodsForm:
    BACK_LINK = "Back to review goods"
    CONFIRM_BUTTON = "Add to Case"
    HEADING = "Check control list classification and add report summary"
