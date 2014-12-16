from ografy.settings import *


#########
# CACHE #
#########

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:0',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        },
    },
    'session': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        },
    }
}


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ografy_db',
        'USER': 'ografy_db_user',
        'PASSWORD': 'foxtrot1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


###########
# MONGODB #
###########

MONGODB_DBNAME = 'ografy_db'
MONGODB_SERVERNAME = 'localhost'
MONGODB_SERVERPORT = 27017


#############
# TEMPLATES #
#############

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
