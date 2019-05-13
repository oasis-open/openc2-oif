import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')

FIXTURE_DIRS = [
    os.path.join(DATA_DIR, 'fixtures')
]

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vcj0le7zphvkzdcmnh7)i2sd(+ba2@k4pahqss&nbbpk4cpk@y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_CHECK = [
    'production' in sys.argv,
    'collectstatic' in sys.argv
]
if any(DEBUG_CHECK):
    DEBUG = False

ALLOWED_HOSTS = ['*']

IP = '0.0.0.0'

PORT = "8080"

SOCKET = f'{IP}:{PORT}'

APPEND_SLASH = True

# Application definition
INSTALLED_APPS = [
    # Custom Modules - MUST BE IN DEPENDENCY ORDER!!
    'orchestrator',
    'account',
    'device',
    'actuator',
    'command',
    'tracking',
    # Default Modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # REST API
    'rest_framework',
    'rest_framework.authtoken',
    # Swagger REST API View
    'rest_framework_swagger',
    # DataTables AJAX Addin
    'rest_framework_datatables',
    # Dynamic config from database
    'dynamic_preferences',
    # Dynamic user config - uncomment to enable
    # 'dynamic_preferences.users.apps.UserPreferencesConfig',
    # CORS (Cross-Origin Resource Sharing)
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orchestrator.middleware.RESTMiddleware',
    'tracking.middleware.LoggingMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'orchestrator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(DATA_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences'
            ]
        }
    }
]

WSGI_APPLICATION = 'orchestrator.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# MySQL/MariaDB
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get('DATABASE_NAME', 'orchestrator'),
        'USER': os.environ.get('DATABASE_USER', 'orc_root'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', '0Rch35Tr@t0r'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '3306'),
        'CON_MAX_AGE': 0
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = []

if DEBUG:
    # Default Static Dir
    STATICFILES_DIRS.append(os.path.join(DATA_DIR, "static"))
    # App Static Dirs
    for app in INSTALLED_APPS:
        app_static_dir = os.path.join(BASE_DIR, app, 'static')
        if os.path.isdir(app_static_dir):
            STATICFILES_DIRS.append(app_static_dir)
else:
    # Central location for all static files
    STATIC_ROOT = os.path.join(DATA_DIR, "static")


MEDIA_URL = '/uploads/'

# Email Config - maybe...
# https://docs.djangoproject.com/en/2.0/topics/email/

# Auth Config
LOGIN_URL = '/account/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/account/logout/'

# Dynamic Preferences
DYNAMIC_PREFERENCES = {
    'REGISTRY_MODULE': 'preferences_registry'
}

# JWT
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS512',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler', # Original
    'JWT_PAYLOAD_HANDLER': 'orchestrator.jwt_handlers.jwt_payload_handler',  # Custom
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',  # Original
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'orchestrator.jwt_handlers.jwt_response_payload_handler',  # Custom
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
    # Not listed in docs, but in example.....
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
}

# Rest API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 10,
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {module} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    }
}

# Tracking
from tracking import REQUEST_LEVELS
TRACKING = {
    'URL_PREFIXES': [
        '^/(?!admin)'  # Don't log /admin/*
    ],
    'REQUEST_LEVELS': [
        REQUEST_LEVELS.Redirect,
        REQUEST_LEVELS.Client_Error,
        REQUEST_LEVELS.Server_Error
    ]
}

# Queue
QUEUE = {
    'hostname': os.environ.get('QUEUE_HOST', 'localhost'),
    'port': os.environ.get('QUEUE_PORT', 5672),
    'auth': {
        'username': os.environ.get('QUEUE_USER', 'guest'),
        'password': os.environ.get('QUEUE_PASSWORD', 'guest')
    },
    'exchange': 'orchestrator',
    'consumer_key': 'response',
    'producer_exchange': 'transport'
}

MESSAGE_QUEUE = None

# GUI Configuration
ADMIN_GUI = True

# JSON Editor - Admin GUI
JSON_EDITOR_JS = f'{STATIC_URL}admin/js/jsoneditor.js'

JSON_EDITOR_CSS = f'{STATIC_URL}admin/css/jsoneditor.css'

# OIF Specific Configurations
PUB_SUB_PROTOS = [
    'MQTT',
]