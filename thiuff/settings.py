"""
Django settings for thiuff project.

Generated by 'django-admin startproject' using Django 1.9.dev20150712143616.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '69gr3dkqo3ke!+c^7lpj!%-9_=bi+h@no5&%7i)ob6c-%#%rs!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'threads',
    'users',
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thiuff.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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
    {
        'BACKEND': 'thiuff.template_backend.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'thiuff.template_backend.environment',
            'extensions': [
                'jinja2.ext.with_',
                'jdj_tags.extensions.DjangoCompat',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thiuff.wsgi.application'

LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thiuff',
        'USER': 'postgres',
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


# Channels

CHANNEL_BACKENDS = {
    "default": {
        "BACKEND": "channels.backends.database.DatabaseChannelBackend",
        "ROUTING": {
            "django.websocket.connect": "threads.consumers.ws_connect",
            "django.websocket.keepalive": "threads.consumers.ws_connect",
            "django.websocket.receive": "threads.consumers.ws_message",
            "django.websocket.disconnect": "threads.consumers.ws_disconnect",
        },
    },
}

WEBSOCKET_URL = "ws://localhost:9000"


# Disallowed group names

DISALLOWED_NAMES = [
    "help",
    "static",
    "site",
    "alpha",
    "beta",
    "test",
    "testing",
    "thiuff",
    "assistance",
    "about",
    "login",
    "log-in",
    "signin",
    "signup",
    "logout",
    "auth",
    "admins",
    "admin",
]
