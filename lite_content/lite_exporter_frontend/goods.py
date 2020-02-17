from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK


class GoodsList:
    TITLE = "Product list"
    CREATE_GOOD = "Add a product"
    GOOD = "Product"
    VERIFIED = "ECJU has verified this product"
    EDIT_GOOD_LINK = "Edit product"
    IN_REVIEW = "ECJU is currently reviewing this product."

    YOUR_GOOD = "Product"
    NO_LONGER_CAN_BE_CHANGED = "This product has been used on an application so can’t be edited."

    class Count:
        ORGANISATION_ZERO = "Your organisation has no products listed."
        ORGANISATION_ONE = "Your organisation has 1 product listed"
        ORGANISATION_MANY = "Your organisation has %s products listed"  # %s will add the count of goods
        FILTERED_ZERO = "No products match your filters"
        FILTERED_ONE = "1 product matches your filters"
        FILTERED_MANY = "%s products match your filters"  # %s will add the count of goods

    class Filter:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "Control list classification"
        PART_NUMBER = generic.PART_NUMBER
        APPLY = "Apply filters"
        CLEAR = "Clear filters"
        SHOW = "Show filters"
        HIDE = "Hide filters"

    class Table:
        DESCRIPTION = generic.DESCRIPTION
        CONTROL_LIST_ENTRY = "CLC"
        IS_GOOD_CONTROLLED = "Controlled"
        PART_NUMBER = generic.PART_NUMBER
        QUANTITY = "Quantity"
        VALUE = "Value"
        INCORPORATED = "Incorporated"
        COUNTRIES = "Countries"
        STATUS = "Status"

    class Documents:
        TITLE = "Documents"
        NO_DOCUMENT_ATTACHED = "There are no documents"
        NAME = "File"
        DESCRIPTION = "Description"
        UPLOADED_BY = "Uploaded by"


class DocumentSensitivityForm:
    TITLE = "Does the product documentation meet the following criteria?"
    DESCRIPTION = (
        "I have a document for my product.\nDocumentation should be specifications, datasheets, sales brochures, "
        "drawings or anything else that fully details what the product is and what it's designed to do.\n\n"
        "The document is below OFFICIAL-SENSITIVE."
    )
    ECJU_HELPLINE = (
        "**<noscript>If the answer is No;</noscript>**\n\nContact ECJU to arrange a more secure way to send "
        "this document.\n\n You can continue with the application "
        "without attaching a document.\n\n **ECJU helpline**\n 020 7215 4594.\n "
        "[Find out about call charges](https://www.gov.uk/call-charges)"
    )
    SUBMIT_BUTTON = "Continue"
    BACK_BUTTON = "Back to product"
    LABEL = "Missing document reason"

    class Options:
        YES = "Yes"
        NO = "No"


class CreateGoodForm:
    TITLE_APPLICATION = "Add a product to your application"
    TITLE_GOODS_LIST = "Add a product to your product list"
    SUBMIT_BUTTON = "Continue"
    BACK_BUTTON = "Back"

    class Description:
        TITLE = generic.DESCRIPTION
        DESCRIPTION = "Start with the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by [military end use controls]"
            "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes]"
            "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        CLC_REQUIRED = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by [military end use controls]"
            "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes]"
            "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know, raise a control list classification (CLC) query"

    class ControlListEntry:
        TITLE = "Control list classification (CLC)"
        DESCRIPTION = "For example, ML1a."

    class IsGraded:
        TITLE = "Does the product have a security grading?"
        DESCRIPTION = "For example, UK OFFICIAL or NATO UNCLASSIFIED"

        YES = "Yes"
        NO = "No, it doesn't need one"
        RAISE_QUERY = "No, it needs one, apply for a private venture (PV) grading"

    class PartNumber:
        TITLE = generic.PART_NUMBER


class GoodGradingForm:
    TITLE = "Security grading"
    DESCRIPTION = ""

    PREFIX = "Prefix"
    GRADING = "Grading"
    SUFFIX = "Suffix"
    OTHER_GRADING = "Other type of security grading"
    ISSUING_AUTHORITY = "Issuing authority"
    REFERENCE = "Reference"
    DATE_OF_ISSUE = "Date of issue"

    BUTTON = "Save and continue"


class GoodsQueryForm:
    TITLE = "Product query"
    DESCRIPTION = ""
    BACK_LINK = "Back to product"
    BUTTON = "Submit"

    class CLCQuery:
        TITLE = "Raise a control list classification (CLC) query"

        class Code:
            TITLE = "What do you think the CLC is for the product?"
            DESCRIPTION = "For example, ML1a."

        class Details:
            TITLE = "Comments"

    class PVGrading:
        TITLE = "Apply for a private venture (PV) grading"

        class Details:
            TITLE = "Comments"

    class Additional:
        TITLE = "Comments"
        DESCRIPTION = "Include details of why you don't know if the product is controlled."


class EditGoodForm:
    TITLE = "Edit product"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description"
        DESCRIPTION = "Start with the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Is the product on the control list?"
        DESCRIPTION = (
            "Products that aren't on the " + PERMISSION_FINDER_LINK + " may be affected by "
            "[military end use controls](https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
            "[current trade sanctions and embargoes](https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
            "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
            "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know, raise a control list classification (CLC) query"

    class ControlListEntry:
        TITLE = "Control list classification (CLC)"
        DESCRIPTION = "For example, ML1a."

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class PartNumber:
        TITLE = "Part number"

    class Buttons:
        SAVE = "Save"
        DELETE = "Delete product"

    class DeleteConfirmationForm:
        TITLE = "Confirm you want to delete this product"
        YES = "Confirm and delete the product"
        NO = "Cancel"


class AttachDocumentForm:
    TITLE = "Attach a document"
    DESCRIPTION = (
        "Documentation could be specifications, datasheets, sales brochures, drawings "
        "or anything else that fully details what the product is and what it's designed to do."
        "\n\nDo not attach a document that’s OFFICIAL-SENSITIVE or above. "
        "\n\nThe file must be smaller than 100MB."
    )
    BUTTON = "Save"
    BACK_FORM_LINK = "Back"
    BACK_GOOD_LINK = "Back to product"

    class Description:
        TITLE = "Description"


class RespondToQueryForm:
    TITLE = "Respond to ECJU query"
    BUTTON = "Submit response"
    BACK_LINK = "Back to product"

    class Response:
        TITLE = "Your response"
        DESCRIPTION = ""

    class ConfirmationForm:
        TITLE = "Confirm you want to send the response"
        BACK_LINK = "Back to edit response"
        YES = "Confirm and send the response"
        NO = "Cancel and change the response"


class GoodPage:
    YOUR_QUERY_HEADING = "Your query"

    class Tabs:
        DETAILS = "Details"
        NOTES = "Notes"
        ECJU_QUERIES = "ECJU queries"
        GENERATED_DOCUMENTS = "ECJU documents"

    class Query:
        TITLE = "Product query"
        CASE_OFFICER = "Case officer"
        NO_ASSIGNED_CASE_OFFICER = "Not assigned"
        REFERENCE = "ECJU reference"
        CLC_RAISED_REASONS = "CLC query reasons"
        GRADING_RAISED_REASONS = "grading query reasons"

    class Document:
        DOWNLOAD = generic.Document.DOWNLOAD
        DELETE = generic.Document.DELETE
        PROCESSING = generic.Document.PROCESSING
        ATTACH = generic.Document.ATTACH
        REMOVE = generic.Document.REMOVE

    class RaiseQuery:
        PREFIX = "If you're not sure it's a controlled product, "
        LINK = "raise a control list classification query"
        SUFFIX = "."

    class Table:
        DESCRIPTION = "Description"
        IS_GOOD_CONTROLLED = "Controlled"
        CONTROL_LIST_ENTRY = "CLC"

        class Grading:
            IS_GRADED = "Security graded"
            GRADING = "Grade"
            REFERENCE = "Reference"
            ISSUING_AUTHORITY = "Issuing authority"
            DATE_OF_ISSUE = "Date of issue"


class AddGoodToApplicationForm:
    TITLE = "Value and quantity of the product"
    DESCRIPTION = ""
    DOCUMENT_MISSING = "Select a document"
    BACK_LINK = "Back to products"

    class Value:
        TITLE = "Value of your products"
        DESCRIPTION = ""

    class VALUE:
        TITLE = "Total value"
        DESCRIPTION = ""

    class Quantity:
        TITLE = "Quantity"
        DESCRIPTION = ""

    class Units:
        TITLE = "Unit of measurement"
        DESCRIPTION = ""

    class Incorporated:
        TITLE = "Will the product be incorporated into another product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"


class AddPreexistingGoodToApplicationForm:
    TITLE = "Select a product from your product list"


class ViewGoodOnApplicationPage:
    TITLE = "Products"
    ADD_NEW_BUTTON = "Add a new product"


class GoodsLocationForm:
    WHERE_ARE_YOUR_GOODS_LOCATED_TITLE = "Where are the products located?"
    WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION = ""
    ONE_OF_MY_REGISTERED_SITES = "At one of my organisation’s sites"
    ONE_OF_MY_REGISTERED_SITES_DESCRIPTION = ""
    NOT_AT_MY_REGISTERED_SITES = "At a location that's not part of my organisation"
    NOT_AT_MY_REGISTERED_SITES_DESCRIPTION = ""
    DEPARTED_THE_COUNTRY = "The products are no longer in the UK"
    DEPARTED_THE_COUNTRY_DESCRIPTION = ""
    EXTERNAL_LOCATION_TITLE = "Do you want to add a new external location or use an existing one?"
    EXTERNAL_LOCATION_NEW_LOCATION = "Add a new external location"
    EXTERNAL_LOCATION_PREEXISTING_LOCATION = "Use an existing external location"
    ERROR = "Select an option"


class GoodsCountriesMatrix:
    BACK = "Back to application overview"
    TITLE = "Select the countries each product is going to"
    ERROR = "Select at least 1 country for each product"
    THIS_IS_OPTIONAL = ""
    SELECT_ALL = "Select all"
    DESELECT_ALL = "Deselect all"
    SAVE = "Save"


class GoodsLocationPage:
    SELECT_SITES_TITLE = "Product locations"
    SELECT_SITES_BUTTON = "Add sites"


class GoodsPage:
    NOTIFICATIONS = "Notifications"


class AttachDocumentPage:
    UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
    UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."


class DeleteGoodDocumentPage:
    TITLE = "Confirm you want to delete this document"
    BACK = "Back to product"
    DOCUMENT_NAME = "Name"
    DOCUMENT_CREATED_AT = "Created at"
    DOCUMENT_CREATED_BY = "Created by"
    DOCUMENT_DESCRIPTION = "Description"
    BUTTON = "Delete document"
