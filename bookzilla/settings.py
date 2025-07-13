import os
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'em3$%7-5m&q7wvq(lwbuh20q7siqn5g808_ih@%gvw2*j!gw54'

DEBUG = True
ALLOWED_HOSTS = []

# Application definition
PREREQ_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ADDON_APPS = (
    'widget_tweaks',
)

PROJECT_APPS = (
    'users',
    'books',
    'bookrequests',
    'courier',
)

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + ADDON_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookzilla.urls'
WSGI_APPLICATION = 'bookzilla.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (book covers, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auth
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/users/home'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users', 'templates'),
            os.path.join(BASE_DIR, 'books', 'templates'),
            os.path.join(BASE_DIR, 'bookrequests', 'templates'),
            os.path.join(BASE_DIR, 'courier', 'templates'),
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
