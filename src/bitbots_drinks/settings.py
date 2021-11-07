"""
Django settings for bitbots_drinks project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

from configurations import Configuration, values
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


class Base(Configuration):
    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.admin",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "drf_spectacular",
        "bitbots_drinks_core",
        "bitbots_drinks_api",
    ]

    MIDDLEWARE = [
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
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
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

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Security relevant settings
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    AUTH_USER_MODEL = "bitbots_drinks_core.User"

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "TITLE": "Bit-Bots Drinks API",
        "DESCRIPTION": "REST-API for the Bit-Bots Drinks service",
        "VERSION": "1.0.0",
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    }

    ###
    # Computed settings
    ###
    @property
    def DATABASES(self):
        # Database
        # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
        return {
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": self.DB_PATH}
        }

    @property
    def EMAIL_BACKEND(self):
        if self.EMAIL_ENABLED and not self.DEBUG:
            return "django.bitbots_drinks_core.mail.backends.smtp.EmailBackend"
        elif self.DEBUG:
            return "django.bitbots_drinks_core.mail.backends.console.EmailBackend"
        else:
            return "django.bitbots_drinks_core.mail.backends.dummy.EmailBackend"

    @property
    def DEFAULT_FROM_MAIL(self):
        return self.EMAIL_FROM

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

    EMAIL_FROM = values.Value(environ_prefix="BBD")
    EMAIL_HOST = values.Value(environ_prefix="BBD")
    EMAIL_PORT = values.IntegerValue(environ_prefix="BBD", default=25)
    EMAIL_HOST_USER = values.Value(environ_prefix="BBD")
    EMAIL_HOST_PASSWORD = values.Value(environ_prefix="BBD")
    EMAIL_USE_TLS = values.BooleanValue(environ_prefix="BBD", default=False)
    EMAIL_USE_SSL = values.BooleanValue(environ_prefix="BBD", default=False)


class Dev(Base):
    SECRET_KEY = "django-insecure-w=wf5uo!qsp=--f18j_wq_uc48813i(7f=ik913*j0j+t-0m5c"
    DEBUG = True
    EMAIL_ENABLED = True

    @classmethod
    def pre_setup(cls):
        os.environ.setdefault(
            "BBD_DB_PATH", str(BASE_DIR.absolute().parent / "db.sqlite")
        )


class Prod(Base):
    DEBUG = False
    SECRET_KEY = values.SecretValue(environ_prefix="BBD")
    ALLOWED_HOSTS = values.ListValue(environ_prefix="BBD", environ_required=True)

    @property
    def EMAIL_ENABLED(self):
        return self.EMAIL_HOST is not None and self.EMAIL_FROM is not None
