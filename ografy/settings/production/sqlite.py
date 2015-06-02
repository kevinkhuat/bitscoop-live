from ografy.settings.production import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_path(ROOT_PATH, 'databases', 'production.db'),
    },
}
