"""
Django settings for HypeBack project.

Generated by "django-admin startproject" using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import urllib.parse

from django.core.management.utils import get_random_secret_key

import environ

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = env.str("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["*"])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_celery_results",
    "django_celery_beat",
    "consumer",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


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
            ],
        },
    },
]


# SLACK SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
SLACK_BOT_TOKEN = env.str("SLACK_BOT_TOKEN", default="")

# APLICATION SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
ROOT_URLCONF = "api.urls"
WSGI_APPLICATION = "api.wsgi.application"


# DIRECTORY SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
STATIC_URL = urllib.parse.urljoin(env.str("STATIC_HOST", default=""), "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "api/static"),
]

MEDIA_HOST = env.str("MEDIA_HOST", default="")
MEDIA_URL = env.str("MEDIA_URL", default="/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# COIN SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
TOKENS_TRANSFER_AMOUNT = env.list("TOKENS_TRANSFER_AMOUNT", default=[1])
TOKENS_URL = env.list("TOKENS_URL", default=[""])
TOKENS_CONTRACT_ADDRESS = env.list("TOKENS_CONTRACT_ADDRESS", default=[""])
TOKENS_ACCOUNT_PRIVATE_KEY = env.list("TOKENS_ACCOUNT_PRIVATE_KEY", default=[""])


# NFT SETTINGS
# ---------------------------------------------------------------------------------------------------------------------
NFTS_URL = env.list("NFTS_URL", default=[""])
NFTS_CONTRACT_ADDRESS = env.list("NFTS_CONTRACT_ADDRESS", default=[""])
NFTS_MAX_AMOUNT = env.list("NFTS_MAX_AMOUNT", default=[0])


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": env.db_url(
        "DATABASE_DEFAULT_URL",
        default="sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite3")),
    ),
}

# Sessions
# ---------------------------------------------------------------------------------------------------------------------
# Cache to store session data if using the cache session backend.
SESSION_CACHE_ALIAS = "sessions"
# The module to store session data
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# A string like "example.com", or None for standard domain cookie.
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", default=None)
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = not DEBUG


# CACHE
# ---------------------------------------------------------------------------------------------------------------------
CACHES = {
    "default": env.cache(
        "CACHES_DEFAULT_URL", default="locmemcache://unique-snowflake"
    ),
    "sessions": env.cache(
        "CACHES_SESSIONS_URL", default="locmemcache://unique-snowflake"
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Celery
# ---------------------------------------------------------------------------------------------------------------------
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_URL = env.list("CELERY_BROKER_URL", default=None)
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_PERSISTENT = True
CELERY_RESULT_BACKEND = "django-db"
