from __future__ import unicode_literals

from ografy.settings.shared import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.ografy.io']

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
