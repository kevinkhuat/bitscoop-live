from __future__ import unicode_literals

from ografy.settings.shared import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ografy.io']

STATIC_URL = '/static/'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'light.db')),
    },
}

# Logging configuration
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

MONGODB_SERVERNAME = 'localhost'

MONGODB_SERVERPORT = 27017

MONGODB_DBNAME = 'ografy_db'