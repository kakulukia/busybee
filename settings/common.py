
import os
from pathlib import Path

from pypugjs.ext.django.compiler import enable_pug_translations

from my_secrets import secrets

enable_pug_translations()

BASE_DIR = Path.cwd()
SECRET_KEY = secrets.SECRET_KEY
SITE_ID = 1

DEBUG = False
ALLOWED_HOSTS = [
    '445a032.online-server.cloud',
    '*.busybee-catering.de',
    'www.busybee-catering.de',
]
INSTALLED_APPS = [
    # our own stuff
    "users",
    'bee',
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # 3rd party apps
    "axes",
    "captcha",
    "compressor",
    "django_extensions",
    "django_secrets",
    "post_office",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'axes.middleware.AxesMiddleware',
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesBackend',
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                # PyPugJS part:   ##############################
                (
                    "pypugjs.ext.django.Loader",
                    (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                )
            ],
            "builtins": ["pypugjs.ext.django.templatetags"],
        },
    }
]

AUTH_USER_MODEL = "users.User"
ROOT_URLCONF = "settings.urls"
WSGI_APPLICATION = "settings.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
    # PLEASE as soon as the project gets a lil more serious => use Postgres!
    # https://duckduckgo.com/?q=postgres+vs+mysql&atb=v101-6&iax=videos&ia=videos&iai=emgJtr9tIME
    #############################################################################################
    #  'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'db_name',
    #     'USER': 'username',
    #     'PASSWORD': secrets.DB_PASSWORD,
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    #     'ATOMIC_REQUESTS': True,  # enables automatic rollback on broken requests
    # }
}
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "axes_cache": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AXES_LOGIN_FAILURE_LIMIT = 2
AXES_CACHE = "axes_cache"
AXES_USE_USER_AGENT = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = "de-de"
TIME_ZONE = "CET"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATICFILES_DIRS = [str(BASE_DIR / "assets")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = str(BASE_DIR / "static")
MEDIA_ROOT = str(BASE_DIR / "media")
COMPRESS_PRECOMPILERS = (("text/x-sass", "django_libsass.SassCompiler"),)
COMPRESS_ENABLED = True


EMAIL_OVERRIDE_ADDRESS = None
EMAIL_FOOTER = ""
EMAIL_BACKEND = "post_office.EmailBackend"
DEFAULT_FROM_EMAIL = "busy.bee@t-online.de"
EMAIL_HOST = "securesmtp.t-online.de"
EMAIL_PORT = 465
EMAIL_HOST_USER = secrets.EMAIL_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_PASSWORD
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
