from ografy.settings.shared import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.ografy.io']

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
STATIC_URL = 'https://static.ografy.io/'