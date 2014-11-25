from ografy.settings import *


#########
# CACHE #
#########

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'session': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'development.db')),
    },
}


#############
# DEBUGGING #
#############

DEBUG = True


###########
# LOGGING #
###########

LOGGING = {}


############
# SECURITY #
############

CSRF_COOKIE_SECURE = False


#############
# TEMPLATES #
#############

TEMPLATE_DEBUG = True


##########
# STATIC #
##########

STATIC_URL = '/static/'


############
# SESSIONS #
############

SESSION_COOKIE_SECURE = False

