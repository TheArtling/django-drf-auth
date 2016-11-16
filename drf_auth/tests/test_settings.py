"""Settings that need to be set in order to run the tests."""
import os


DEBUG = True
SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'drf_auth.tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../app_static')
MEDIA_ROOT = os.path.join(APP_ROOT, '../app_media')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [os.path.join(APP_ROOT, 'tests/test_app/templates')],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
        )
    }
}]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'rest_framework',
]

INTERNAL_APPS = [
    'drf_auth',
    'drf_auth.tests.test_app',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'drf_auth.middleware.FinishSignupMiddleware',
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "drf_auth.auth_backends.DRFAuthAuthenticationBackend",
)

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1'],
}

SECRET_KEY = 'foobar'

from .local_settings import *  # NOQA
