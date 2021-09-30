"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG') == 'True'

ALLOWED_HOSTS = [
    'api-ifu.voxastro.org',
    'api-ifu.sai.msu.ru',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'rest_framework',
    'silk',
    'ifuapp',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'website.urls'

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

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST = [
    "https://ifu.voxastro.org",
    "https://ifu.sai.msu.ru",
]

GRAPHENE = {
    "SCHEMA": "ifuapp.schema.schema",
    # defaults to schema.json,
    'SCHEMA_OUTPUT': os.path.join(STATIC_ROOT, 'schema.json'),
    # Defaults to None (displays all data on a single line)
    'SCHEMA_INDENT': 2,
}


if DEBUG:
    CORS_ORIGIN_WHITELIST += [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://localhost:8080",
        "http://localhost:8081",
    ]
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost', 'testserver']


    # too slow... likely related to
    # https://github.com/jazzband/django-debug-toolbar/issues/1402

    # MIDDLEWARE += [
    #     'debug_toolbar.middleware.DebugToolbarMiddleware',
    #     # 'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',
    # ]
    # INSTALLED_APPS += [
    #     'debug_toolbar',
    #     # 'graphiql_debug_toolbar',
    # ]

    # import socket
    # INTERNAL_IPS = ['127.0.0.1']
    # hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    # INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

    # PRETTIFY_SQL = False
    # this is the main reason for not showing up the toolbar
    # import mimetypes
    # mimetypes.add_type("application/javascript", ".js", True)

    # DEBUG_TOOLBAR_CONFIG = {
    #     'INTERCEPT_REDIRECTS': False,
    # }

# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': (
#         'drf_ujson.renderers.UJSONRenderer',
#     ),
# }
sip = os.getenv('SILKY_INTERCEPT_PERCENT')
SILKY_INTERCEPT_PERCENT = 0 if sip is None else int(sip)
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_META = True
SILKY_ANALYZE_QUERIES = True
SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'profs')
SILKY_DYNAMIC_PROFILING = [
    {
        'module': 'ifuapp.models.cube.CubeViewSet',
        'function': 'list'
    },
    {
        'module': 'ifuapp.models.cube.Cube2ViewSet',
        'function': 'list'
    },
    {
        'module': 'ifuapp.models.cube.Cube3ViewSet',
        'function': 'list'
    },
]
