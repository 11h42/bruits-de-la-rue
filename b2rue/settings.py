# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

import os
from configparser import ConfigParser, NoSectionError
import sys

from django.contrib import messages


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING_PATH = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

CONFIG_PATH = os.path.join(BASE_DIR, 'config')
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.ini')

config = ConfigParser()
config.read(CONFIG_FILE)

try:
    SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')
except:
    print('SECRET_KEY not found! Generating a new one...')
    import random

    SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
    if not config.has_section('DJANGO'):
        config.add_section('DJANGO')
    config.set('DJANGO', 'SECRET_KEY', SECRET_KEY)
    with open(CONFIG_FILE, 'wt') as configfile:
        config.write(configfile)

try:
    DEBUG = config.getboolean('DEBUG', 'DEBUG')
except NoSectionError:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'frontend',
    'crispy_forms'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'b2rue.urls'

WSGI_APPLICATION = 'b2rue.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE', 'ENGINE'),
        'NAME': config.get('DATABASE', 'NAME'),
        'USER': config.get('DATABASE', 'USER'),
        'PASSWORD': config.get('DATABASE', 'PASSWORD'),
        'HOST': config.get('DATABASE', 'HOST'),
        'PORT': config.get('DATABASE', 'PORT')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'static'),
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

AUTH_USER_MODEL = 'core.User'

DEFAULT_FROM_EMAIL = config.get('EMAIL', 'DEFAULT_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_HOST = config.get('EMAIL', 'SMTP_HOST')

# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = config.get('EMAIL', 'SMTP_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL', 'SMTP_PASSWORD')
EMAIL_USE_TLS = True

TESTS_IN_PROGRESS = False
if 'test' in sys.argv[1:] or 'jenkins' in sys.argv[1:]:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    TESTS_IN_PROGRESS = True