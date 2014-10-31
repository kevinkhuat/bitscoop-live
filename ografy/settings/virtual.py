from __future__ import unicode_literals

from ografy.settings.production import *


DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.ografy.io', 'localhost']

STATIC_URL = 'https://virtual.static.ografy.io/'
