import os
from datetime import timedelta

from decouple import config
from django.conf import settings

from .base import (
    INSTALLED_APPS, MIDDLEWARE,
    STATIC_ROOT, BASE_DIR, STATICFILES_DIRS
)

# ############## #
#   EXTENSIONS   #
# ############## #

# admin
INSTALLED_APPS.append('django.contrib.admindocs')
INSTALLED_APPS.append('django.contrib.sites')
INSTALLED_APPS.append('django.contrib.postgres')

ELASTICSEARCH_ENABLED = config('ELASTICSEARCH_ENABLED', cast=bool, default=False)

# packages
INSTALLED_APPS.append('rest_framework')
INSTALLED_APPS.append('corsheaders')
INSTALLED_APPS.append('admin_footer')
INSTALLED_APPS.append('admin_honeypot')
INSTALLED_APPS.append('django_filters')
INSTALLED_APPS.append('cachalot')
INSTALLED_APPS.append('drf_yasg')
INSTALLED_APPS.append('mptt')
if ELASTICSEARCH_ENABLED:
    INSTALLED_APPS.append('django_elasticsearch_dsl')

# Log

# Security

# Applications
INSTALLED_APPS.append('categories')
INSTALLED_APPS.append('products')
INSTALLED_APPS.append('carts')
INSTALLED_APPS.append('discounts')
INSTALLED_APPS.append('search')

# ###################### #
#     REST FRAMEWORK     #
# ###################### #

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # TODO: Should be removed in production
    ),
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '30/minute'
    # },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'SEARCH_PARAM': 'query'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',  # change to RS512 in production
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': 'owner',
    'ISSUER': 'phonebook.com',

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'username',
    'USER_ID_CLAIM': 'identity',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ########## #
#   CACHE    #
# ########## #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_HOST')
    }
}
CACHE_TIMEOUT = 3600

# ########### #
#   UPLOAD    #
# ########### #
# FILE_UPLOAD_HANDLERS = [
#     'painless.utils.handlers.upload.ChunkFileUploadHandler'
# ]
# UPLOAD_CHUNK_SIZE = 2500 * 2 ** 10  # 2500 KB

# ######################### #
#       AdminInterface      #
# ######################### #
from datetime import datetime

ADMIN_FOOTER_DATA = {
    'site_url': 'https://shop.com',
    'site_name': 'SHOP',
    'period': '{}'.format(datetime.now().year),
    'version': 'v0.0.1 - development'
}

# #################### #
# IMPORTANT VARIABLES  #
# #################### #
# AUTH_USER_MODEL = 'accounts.CustomUser'

# ########################### #
#     DJANGO CORS HEADERS     #
# ########################### #
from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods

CORS_ALLOW_HEADERS = list(default_headers)
CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True  # TODO: should be changed in production

CACHALOT_UNCACHABLE_APPS = ('admin', 'auth',)

# Elasticsearch
# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html
if ELASTICSEARCH_ENABLED:
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': config('ELASTICSEARCH_HOST', default='localhost:9200'),
        },
    }
