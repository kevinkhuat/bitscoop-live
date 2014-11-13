from __future__ import unicode_literals

from ografy.settings.production import *


DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.ografy.io', 'localhost']

STATIC_URL = 'https://virtual.static.ografy.io/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.abspath(os.path.join(ROOT_PATH, '..', 'logs', 'debug.log')),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

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
