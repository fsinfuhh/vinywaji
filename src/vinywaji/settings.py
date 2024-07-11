"""
Django settings for vinywaji project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from ipaddress import ip_network
from pathlib import Path

from environs import Env

# Access runtime settings via `MY_SETTING = env.str("MY_SETTING")` (or user other types e.g. `env.bool()`)
env = Env()
env.read_env(".env", override=True)
env.read_env(".env.local", override=True)
APP_MODE = env.str("APP_MODE", default="dev")
env.read_env(f".env.{APP_MODE}", override=True)
env.read_env(f".env.{APP_MODE}.local", override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

###
# Runtime customizable settings
###
DEBUG = env.bool("VW_DEBUG", default=False)
SERVED_OVER_HTTPS = env.bool("VW_SERVED_OVER_HTTPS", default=False)
TRUST_REVERSE_PROXY = env.bool("VW_TRUST_REVERSE_PROXY", default=False)
SECRET_KEY = env.str("VW_SECRET_KEY")
ALLOWED_HOSTS = env.list("VW_ALLOWED_HOSTS")
ALLOWED_METRICS_NETS = [
    ip_network(i) for i in env.list("VW_ALLOWED_METRICS_NETS", default=["127.0.0.0/8", "::/64"])
]
NPM_BIN_PATH = "/usr/bin/npm"

DATABASES = {"default": env.dj_db_url("VW_DB")}
CACHES = {"default": env.dj_cache_url("VW_CACHE", default="dummy://" if DEBUG else "locmem://")}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "whitenoise.runserver_nostatic",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "mathfilters",
    "simple_openid_connect.integrations.django",
    "vinywaji.core",
    "vinywaji.api",
    "vinywaji.gui",
    "vinywaji.metrics",
    "macros",
    "tailwind",
]

if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_openid_connect.integrations.django.middleware.TokenVerificationMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "vinywaji.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

TAILWIND_APP_NAME = "vinywaji.gui"

WSGI_APPLICATION = "vinywaji.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = str(BASE_DIR.parent / "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security relevant settings
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

CSRF_COOKIE_HTTPONLY = True

AUTH_USER_MODEL = "vinywaji_core.User"
LOGIN_URL = "simple_openid_connect:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

OPENID_PROVIDER_NAME = env.str("VW_OPENID_PROVIDER_NAME", default="mafiasi")
OPENID_ISSUER = env.str("VW_OPENID_ISSUER", default="https://identity.mafiasi.de/realms/mafiasi")
OPENID_CLIENT_ID = env.str("VW_OPENID_CLIENT_ID")
OPENID_CLIENT_SECRET = env.str("VW_OPENID_CLIENT_SECRET")
OPENID_SCOPE = env.str("VW_OPENID_SCOPE")

SILENCED_SYSTEM_CHECKS = ["security.W003"]

VERSION = "2.0.0"

ORG_NAME = env.str("VW_ORG_NAME", default="Bit-Bots Drinks")

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TITLE": "{} API".format(ORG_NAME),
    "DESCRIPTION": "REST-API for the {} service".format(ORG_NAME),
    "VERSION": VERSION,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "simple_openid_connect.integrations.djangorestframework.authentication.AccessTokenAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "COMPONENT_SPLIT_PATCH": False,
    "SERVE_INCLUDE_SCHEMA": False,
    "VERSION": VERSION,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "SWAGGER_UI_OAUTH2_CONFIG": {
        "scopes": OPENID_SCOPE,
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG" if DEBUG else "INFO",
        },
    },
}

INTERNAL_IPS = [
    "127.0.0.1",
]

DEFAULT_AMOUNT = env.float("VW_DEFAULT_AMOUNT", default=1.5)
MAFIASI_COLORS = env.bool("VW_MAFIASI_COLORS", default=False)

if SERVED_OVER_HTTPS:
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = env.int("VW_HSTS_SECONDS", default=63072000)

if TRUST_REVERSE_PROXY:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
