from ografy.settings.shared import *

DEBUG = True
TEMPLATE_DEBUG = True

STATIC_URL = '/static/'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'light.db')),
    },
}
