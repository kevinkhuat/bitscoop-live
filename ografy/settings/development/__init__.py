from ografy.settings import *


#########
# CACHE #
#########

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default',
    },
    'session': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'session',
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
MONGODB = {
    'NAME': 'ografy_db',
    'HOST': 'localhost',
    'PORT': 27017,
    # 'SSL_CERT_FILE': 'PLACEHOLDER',
    # 'SSL_CERT_REQS': ssl.CERT_REQUIRED,
    # 'SSL_CA_CERTS': 'PLACEHOLDER',
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


STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(ROOT_PATH, '..', 'build', 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

############
# SESSIONS #
############

SESSION_COOKIE_SECURE = False
