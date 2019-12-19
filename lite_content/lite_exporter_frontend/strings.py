from conf.settings import env
from lite_content.lite_exporter_frontend import applications, goods, roles, users, sites, core, end_users

APPLICATIONS = applications
CORE = core
END_USERS = end_users
GOODS = goods
ROLES = roles
SITES = sites
USERS = users

# Generic (used as defaults in forms)
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
CANCEL = "Cancel"
POST_NOTE = "Post note"

THIS_SECTION_IS = "This section is "  # The space at the end is intentional. Usage is 'This section is optional'
OPTIONAL = "Optional"
NOT_STARTED = "Not started"
IN_PROGRESS = "In progress"
DONE = "Completed"
VIEW = "View"

SUBMIT_APPLICATION = "Submit application"
EDIT_APPLICATION_SUBMIT = "Submit application"
EDIT_APPLICATION_DONE = "Done"

# Constants
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"

UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
DOWNLOAD_GENERIC_ERROR = "We had an issue downloading your file. Try again later."

DOCUMENT_DELETE_GENERIC_ERROR = "We had an issue deleting your files. Try again later."
