class PartyForm:
    class Options:
        GOVERNMENT = "Government organisation"
        COMMERCIAL = "Commercial organisation"
        INDIVIDUAL = "An individual"
        OTHER = "Other"


class EndUserForm:
    TITLE = "Who is the end user of your goods?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class UltimateEndUserForm:
    TITLE = "Who is the ultimate end user of your goods?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Name"
    WEBSITE_FORM_TITLE = "Website address (optional)"
    ADDRESS_FORM_TITLE = "Address"
    SUBMIT_BUTTON = "Save and continue"


class ConsigneeForm:
    TITLE = "Who will be the consignee of your goods?"
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
