from lite_content.lite_exporter_frontend import generic


class ThirdPartiesPage:
    TITLE = "Third parties"
    ADD = "Add a third party"
    NO_RESULTS = "You haven't added any third parties to your application"

    class Variables:
        NAME = "Name"
        TYPE = "Type"
        WEBSITE = "Website"
        ADDRESS = "Address"
        COUNTRY = "Country"
        DOCUMENT = "Document"


class UltimateEndUsers:
    BACK = "Back to application overview"
    TITLE = "Ultimate recipients"
    HELP = "What is an ultimate recipient?"
    DESCRIPTION = (
        "An ultimate recipient is an entity that uses the product or the higher level system into which the products are"
        " installed or incorporated. The end user and ultimate recipient may be different entities."
    )
    NOTICE = "You haven't added any ultimate recipients to this application"
    MISSING_DOCS_NOTICE = "You still need to attach a document to some ultimate recipients"
    ADD_BUTTON = "Add an ultimate recipient"

    class Document:
        DOWNLOAD = generic.Document.DOWNLOAD
        DELETE = generic.Document.DELETE
        PROCESSING = generic.Document.PROCESSING
        ATTACH = generic.Document.ATTACH
        REMOVE = generic.Document.REMOVE
