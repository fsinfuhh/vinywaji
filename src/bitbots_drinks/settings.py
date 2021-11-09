"""
Django settings for bitbots_drinks project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

from configurations import Configuration, values
from django_auth_mafiasi.configuration import BaseAuthConfigurationMixin, DevAuthConfigurationMixin
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


class Base(BaseAuthConfigurationMixin, Configuration):
    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.admin",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "whitenoise.runserver_nostatic",
        "rest_framework",
        "rest_framework.authtoken",
        "drf_spectacular",
        "bitbots_drinks_core",
        "bitbots_drinks_api",
    ] + BaseAuthConfigurationMixin.MAFIASI_AUTH_APPS

    MIDDLEWARE = [
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "bitbots_drinks.urls"

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

    WSGI_APPLICATION = "bitbots_drinks.wsgi.application"

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

    AUTH_USER_MODEL = "bitbots_drinks_core.User"

    AUTH_SCOPE = ["openid", "profile"]

    REST_FRAMEWORK_REQUIRED_SCOPES = AUTH_SCOPE

    LOGIN_REDIRECT_URL = "/api/schema/swagger"

    SILENCED_SYSTEM_CHECKS = ["security.W003"]

    VERSION = "1.0.0"

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "TITLE": "Bit-Bots Drinks API",
        "DESCRIPTION": "REST-API for the Bit-Bots Drinks service",
        "VERSION": VERSION,
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.TokenAuthentication",
            "bitbots_drinks_api.authentication.ServiceAccountAuthentication",
        ],
    }

    SPECTACULAR_SETTINGS = {
        "COMPONENT_SPLIT_PATCH": False,
        "SERVE_INCLUDE_SCHEMA": False,
        "VERSION": VERSION,
        "CONTACT": {"name": "Bit-Bots", "url": "https://bit-bots.de", "email": "info@bit-bots.de"},
    }

    ###
    # Computed settings
    ###
    @property
    def DATABASES(self):
        # Database
        # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
        return {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": self.DB_PATH}}

    @property
    def SESSION_COOKIE_SECURE(self):
        return self.SERVED_OVER_HTTPS

    @property
    def SECURE_SSL_REDIRECT(self):
        return self.SERVED_OVER_HTTPS

    @property
    def SECURE_HSTS_SECONDS(self):
        if self.SERVED_OVER_HTTPS:
            return self.HSTS_SECONDS
        return 0

    @property
    def SECURE_PROXY_SSL_HEADER(self):
        return ("HTTP_X_FORWARDED_PROTO", "https") if self.TRUST_REVERSE_PROXY else None

    @property
    def USE_X_FORWARDED_HOST(self):
        return self.TRUST_REVERSE_PROXY

    @property
    def USE_X_FORWARDED_PORT(self):
        return self.TRUST_REVERSE_PROXY

    @property
    def SESSION_COOKIE_SECURE(self):
        return self.SERVED_OVER_HTTPS

    ###
    # Runtime customizable settings
    ###
    DB_PATH = values.Value(environ_prefix="BBD", environ_required=True)
    SERVED_OVER_HTTPS = values.BooleanValue(environ_prefix="BBD", default=False)
    HSTS_SECONDS = values.IntegerValue(environ_prefix="BBD", default=63072000)
    TRUST_REVERSE_PROXY = values.BooleanValue(environ_prefix="BBD", default=False)
    SERVICE_ACCOUNT_TOKEN = values.SecretValue(environ_prefix="BBD", environ_required=True)


class Dev(DevAuthConfigurationMixin, Base):
    SECRET_KEY = "django-insecure-w=wf5uo!qsp=--f18j_wq_uc48813i(7f=ik913*j0j+t-0m5c"
    DEBUG = True

    @classmethod
    def pre_setup(cls):
        os.environ.setdefault("BBD_DB_PATH", str(BASE_DIR.absolute().parent / "db.sqlite"))
        os.environ.setdefault("BBD_SERVICE_ACCOUNT_TOKEN", "insecure-foobar123")


class Prod(Base):
    DEBUG = False
    SECRET_KEY = values.SecretValue(environ_prefix="BBD")
    ALLOWED_HOSTS = values.ListValue(environ_prefix="BBD", environ_required=True)
