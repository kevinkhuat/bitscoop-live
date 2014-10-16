from __future__ import unicode_literals

from ografy.settings.shared import *


DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'dev.ogrfy.io', 'developer.ografy.io']

STATIC_URL = '/static/'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'development.db')),
    },
}
