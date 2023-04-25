import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'celery',
    'corsheaders',
]

MY_APPS = [
    'authority',
    'portal',
    'eva',
    'control_panel',
    'eva.isiao',
    'eva.reports',
]

DOC_APPS = [
    'drf_spectacular',
]

INSTALLED_APPS += MY_APPS
INSTALLED_APPS += DOC_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'portal.wsgi.application'

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1', 'http://192.168.198.250', 'http://localhost', 'http://192.168.198.84', ]
CORS_ALLOW_ALL_ORIGIN = True

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.198.250',
    'http://localhost',  # for localhost (REACT Default)
    'http://192.168.0.50',  # for network
    'http://localhost',  # for localhost (Developlemt)
    'http://192.168.0.50',  # for network (Development)
]

AUTH_USER_MODEL = 'authority.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}

ZAMMAD_DB_NAME = env('ZAMMAD_DB_NAME')
ZAMMAD_DB_USER = env('ZAMMAD_DB_USER')
ZAMMAD_DB_PASSWORD = env('ZAMMAD_DB_PASSWORD')
ZAMMAD_DB_HOST = env('ZAMMAD_DB_HOST')
ZAMMAD_DB_PORT = env('ZAMMAD_DB_PORT')

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%Y-%m-%d', ]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_IMPORTS = ['eva.isiao.tasks', ]

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = 'Europe/Moscow'

IAS_URL = env('IAS_URL')
IAS_TOKEN = env('IAS_TOKEN')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated',],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Портал для сотрудников ССПК',
    'DESCRIPTION': 'Портал для сотрудников ССПК. Оптимизирует и автоматизирует рутинные задачи',
    'VERSION': '1.0.0',
}

