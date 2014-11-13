from __future__ import unicode_literals

from ografy.settings.shared import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'dev.ografy.io', 'developer.ografy.io', 'virtual.ografy.io']

STATIC_URL = '/static/'

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
