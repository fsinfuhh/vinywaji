"""
Django settings for vinywaji project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env(env.path("BBD_ENV_FILE", default=".env"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

###
# Runtime customizable settings
###
DEBUG = env.bool("BBD_DEBUG", default=False)
SERVED_OVER_HTTPS = env.bool("BBD_SERVED_OVER_HTTPS", default=False)
TRUST_REVERSE_PROXY = env.bool("BBD_TRUST_REVERSE_PROXY", default=False)
SECRET_KEY = env.str("BBD_SECRET_KEY")
ALLOWED_HOSTS = env.list("BBD_ALLOWED_HOSTS")

DATABASES = {"default": env.dj_db_url("BBD_DB")}
CACHES = {"default": env.dj_cache_url("BBD_CACHE", default="dummy://" if DEBUG else "locmem://")}

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
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
LOGIN_URL = "simple_openid_connect_django:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

OPENID_ISSUER = env.str("BBD_OPENID_ISSUER", default="https://identity.mafiasi.de/realms/mafiasi")
OPENID_CLIENT_ID = env.str("BBD_OPENID_CLIENT_ID")
OPENID_CLIENT_SECRET = env.str("BBD_OPENID_CLIENT_SECRET")
OPENID_SCOPE = "openid profile bitbots-drink-transactions"

SILENCED_SYSTEM_CHECKS = ["security.W003"]

VERSION = "2.0.0"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TITLE": "Mafiasi Drinks API",
    "DESCRIPTION": "REST-API for the Mafiasi Drinks service",
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
    "CONTACT": {"name": "Bit-Bots", "url": "https://bit-bots.de", "email": "info@bit-bots.de"},
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

DEFAULT_AMOUNT = env.float("BBD_DEFAULT_AMOUNT", default=1.5)
MAFIASI_COLORS = env.bool("BBD_MAFIASI_COLORS", default=True)

if SERVED_OVER_HTTPS:
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = env.int("BBD_HSTS_SECONDS", default=63072000)

if TRUST_REVERSE_PROXY:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
