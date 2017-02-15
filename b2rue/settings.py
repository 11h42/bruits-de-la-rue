import os
import logging

import sys

from django.contrib import messages
from smartconfigparser import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, 'config')
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.ini')
config = Config()
config.read(CONFIG_FILE)

try:
    SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')
except:
    print('SECRET_KEY not found! Generating a new one...')
    import random

    SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)") for i in range(50)])
    if not config.has_section('DJANGO'):
        config.add_section('DJANGO')
    config.set('DJANGO', 'SECRET_KEY', SECRET_KEY)
    with open(CONFIG_FILE, 'wt') as f:
        config.write(f)

DEBUG = config.getboolean('DJANGO', 'DEBUG', False)

ALLOWED_HOSTS = config.getlist('DJANGO', 'ALLOWED_HOSTS', ['localhost', '127.0.0.1'])

DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE', 'engine', 'django.db.backends.sqlite3'),
        'NAME': config.get('DATABASE', 'name', 'db.sqlite3'),
        'USER': config.get('DATABASE', 'user', ''),
        'PASSWORD': config.get('DATABASE', 'password', ''),
        'HOST': config.get('DATABASE', 'host', ''),
        'PORT': config.get('DATABASE', 'port', ''),
    }
}

LOGGING_PATH = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'frontend',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'b2rue.urls'

WSGI_APPLICATION = 'b2rue.wsgi.application'

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'static'),
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# ALLAUTH configuration
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

AUTH_USER_MODEL = 'core.User'

DEFAULT_FROM_EMAIL = config.get('EMAIL', 'DEFAULT_FROM_EMAIL', 'contact@action-assos.fr')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

DEBUG_EMAIL = config.getboolean('DJANGO', 'DEBUG_EMAIL', False)
if DEBUG_EMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = config.get('EMAIL', 'SMTP_HOST', 'localhost')

# Port for sending e-mail.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = config.get('EMAIL', 'SMTP_USER', 'contact@action-assos.fr')
EMAIL_HOST_PASSWORD = config.get('EMAIL', 'SMTP_PASSWORD', 'password')
EMAIL_USE_TLS = False

TESTS_IN_PROGRESS = False
if 'test' in sys.argv[1:] or 'jenkins' in sys.argv[1:]:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    TESTS_IN_PROGRESS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(name)-14s: %(levelname)-8s %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_PATH, 'b2rue.log'),
            'maxBytes': 1024 * 1024 * 10,
            'formatter': 'simple',
            'backupCount': 5
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'INFO',
        },
        'b2rue': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    }
}

try:
    logging.config.dictConfig(LOGGING)
except Exception as e:
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    print('could not setup logging properly, use basic logging system...')
