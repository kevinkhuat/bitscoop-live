from __future__ import unicode_literals

from ografy.settings.shared import *
from ografy.settings.signals import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.ografy.io', 'localhost']

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
STATIC_URL = 'https://static.ografy.io/'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'production.db')),
    },
}

print(ROOT_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
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
