import os

from environ import Env
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

WSGI_APPLICATION = "conf.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "svg",
    "lite_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.auth.middleware.AuthbrokerClientMiddleware",
    "core.middleware.UploadFailedMiddleware",
    "core.middleware.RequestsSessionMiddleware",
]

# configuration is difficult so omit this when running locally
if not DEBUG:
    MIDDLEWARE += [
        "csp.middleware.CSPMiddleware",
    ]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", True)
SESSION_COOKIE_NAME = env.str("SESSION_COOKIE_NAME", default="exporter")
TOKEN_SESSION_KEY = env.str("TOKEN_SESSION_KEY")

# messages
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/assets/"


# Authbroker config
AUTHBROKER_URL = env.str("AUTHBROKER_URL")
AUTHBROKER_CLIENT_ID = env.str("AUTHBROKER_CLIENT_ID")
AUTHBROKER_CLIENT_SECRET = env.str("AUTHBROKER_CLIENT_SECRET")

HAWK_AUTHENTICATION_ENABLED = env.bool("HAWK_AUTHENTICATION_ENABLED", False)
HAWK_RECEIVER_NONCE_EXPIRY_SECONDS = 60

LOGIN_URL = reverse_lazy("auth:login")

DATA_DIR = os.path.dirname(BASE_DIR)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Cache static files
STATICFILES_STORAGE = env.str("STATICFILES_STORAGE", "whitenoise.storage.CompressedManifestStaticFilesStorage")

# File Upload
# https://github.com/uktrade/s3chunkuploader
S3_DOCUMENT_ROOT_DIRECTORY = ""
S3_APPEND_DATETIME_ON_UPLOAD = True
S3_PREFIX_QUERY_PARAM_NAME = ""
S3_DOWNLOAD_LINK_EXPIRY_SECONDS = 180
STREAMING_CHUNK_SIZE = 8192
S3_MIN_PART_SIZE = 5 * 1024 * 1024
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# AWS
VCAP_SERVICES = env.json("VCAP_SERVICES", {})

if VCAP_SERVICES:
    if "aws-s3-bucket" not in VCAP_SERVICES:
        raise Exception("S3 Bucket not bound to environment")

    aws_credentials = VCAP_SERVICES["aws-s3-bucket"][0]["credentials"]
    AWS_ACCESS_KEY_ID = aws_credentials["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = aws_credentials["aws_secret_access_key"]
    AWS_REGION = aws_credentials["aws_region"]
    AWS_STORAGE_BUCKET_NAME = aws_credentials["bucket_name"]
else:
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = env.str("AWS_REGION")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "(asctime)(levelname)(message)(filename)(lineno)(threadName)(name)(thread)(created)(process)(processName)(relativeCreated)(module)(funcName)(levelno)(msecs)(pathname)",  # noqa
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json",},},
    "loggers": {"": {"handlers": ["console"], "level": env.str("LOG_LEVEL", "INFO")},},
}

# Enable security features in hosted environments

SECURE_HSTS_ENABLED = env.bool("SECURE_HSTS_ENABLED", False)
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 if SECURE_HSTS_ENABLED else None  # 1 year
SECURE_BROWSER_XSS_FILTER = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG
SESSION_EXPIRE_SECONDS = env.int("SESSION_EXPIRE_SECONDS", default=60 * 60)

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = not DEBUG

X_FRAME_OPTIONS = "SAMEORIGIN"

# Content Security Policy

CSP_DEFAULT_SRC = env.tuple("CSP_DEFAULT_SRC", default=("'self'",))
CSP_STYLE_SRC = env.tuple("CSP_STYLE_SRC", default=("'self'",))
CSP_SCRIPT_SRC = env.tuple("CSP_SCRIPT_SRC", default=("'self'",))
CSP_FONT_SRC = env.tuple("CSP_FONT_SRC", default=("'self'",))
CSP_REPORT_ONLY = env.bool("CSP_REPORT_ONLY", False)
CSP_INCLUDE_NONCE_IN = env.tuple("CSP_INCLUDE_NONCE_IN", default=("script-src",))

# Application Performance Monitoring
if env.str("ELASTIC_APM_SERVER_URL", ""):
    ELASTIC_APM = {
        "SERVICE_NAME": env.str("ELASTIC_APM_SERVICE_NAME", "lite-internal-frontend"),
        "SECRET_TOKEN": env.str("ELASTIC_APM_SECRET_TOKEN"),
        "SERVER_URL": env.str("ELASTIC_APM_SERVER_URL"),
        "ENVIRONMENT": env.str("SENTRY_ENVIRONMENT"),
        "DEBUG": DEBUG,
    }
    INSTALLED_APPS.append("elasticapm.contrib.django")

if DEBUG:
    import pkg_resources

    try:
        pkg_resources.get_distribution("django_extensions")
    except pkg_resources.DistributionNotFound:
        pass
    else:
        INSTALLED_APPS.append("django_extensions")
    try:
        pkg_resources.get_distribution("django_pdb")
    except pkg_resources.DistributionNotFound:
        pass
    else:
        INSTALLED_APPS.append("django_pdb")
        POST_MORTEM = False
        MIDDLEWARE.append("django_pdb.middleware.PdbMiddleware")

# Sentry
if env.str("SENTRY_DSN", ""):
    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        environment=env.str("SENTRY_ENVIRONMENT"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

LITE_API_URL = env.str("LITE_API_URL")

PERMISSIONS_FINDER_URL = env.str("PERMISSIONS_FINDER_URL")

if env.str("DIRECTORY_SSO_API_CLIENT_BASE_URL", ""):
    DIRECTORY_SSO_API_CLIENT_API_KEY = env("DIRECTORY_SSO_API_CLIENT_API_KEY")
    DIRECTORY_SSO_API_CLIENT_BASE_URL = env("DIRECTORY_SSO_API_CLIENT_BASE_URL")
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = 30
    DIRECTORY_SSO_API_CLIENT_SENDER_ID = "lite"


FEATURE_DEBUG_TOOLBAR_ON = env.bool("FEATURE_DEBUG_TOOLBAR_ON", False)

if FEATURE_DEBUG_TOOLBAR_ON:
    INSTALLED_APPS += ["debug_toolbar", "requests_panel"]
    DEBUG_TOOLBAR_PANELS = [
        "requests_panel.panel.RequestsDebugPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    index = MIDDLEWARE.index("django.middleware.gzip.GZipMiddleware")
    MIDDLEWARE.insert(index + 1, "debug_toolbar.middleware.DebugToolbarMiddleware")
