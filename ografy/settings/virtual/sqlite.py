from ografy.settings.virtual import *


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'virtual.db')),
    },
}
