"""
Django settings for b2rue project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# CONSTANTS
import sys

DEFAULT_BID_PHOTO = 'images/default.png'



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from tools.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

LOGGING_PATH = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

CONFIG_PATH = os.path.join(BASE_DIR, 'config')
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.ini')

config = Config()
config.read(CONFIG_FILE)

try:
    SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')
except:
    print 'SECRET_KEY not found! Generating a new one...'
    import random

    SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
    if not config.has_section('DJANGO'):
        config.add_section('DJANGO')
    config.set('DJANGO', 'SECRET_KEY', SECRET_KEY)
    f = file(CONFIG_FILE, 'wt')
    config.write(f)
    f.close()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('DEBUG', 'DEBUG', False)
TEMPLATE_DEBUG = config.getboolean('DEBUG', 'TEMPLATE_DEBUG', DEBUG)

ALLOWED_HOSTS = config.get('DJANGO', 'ALLOWED_HOSTS', '').split(';')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'south',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'core.User'

ROOT_URLCONF = 'b2rue.urls'

WSGI_APPLICATION = 'b2rue.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE', 'ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': config.get('DATABASE', 'NAME', 'b2rue'),
        'USER': config.get('DATABASE', 'USER', 'b2rue'),
        'PASSWORD': config.get('DATABASE', 'PASSWORD', ''),
        'HOST': config.get('DATABASE', 'HOST', 'localhost'),
        'PORT': config.get('DATABASE', 'PORT', '5432'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


WWW_PATH = os.path.join(BASE_DIR, 'www')
if not os.path.exists(WWW_PATH):
    os.makedirs(WWW_PATH)

MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

MEDIA_DIR = '/media/'
MEDIA_URL = MEDIA_DIR

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'core/../frontend/templates'),
)

TESTS_IN_PROGRESS = False
if 'test' in sys.argv[1:] or 'jenkins' in sys.argv[1:]:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    DEBUG = False
    TEMPLATE_DEBUG = False
    SOUTH_TESTS_MIGRATE = False
    SKIP_SOUTH_TESTS = True
    TESTS_IN_PROGRESS = True