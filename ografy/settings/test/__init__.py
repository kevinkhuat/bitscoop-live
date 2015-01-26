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


##########
# MODELS #
##########

INSTALLED_APPS += (
    'ografy.tests.test_obase',
    'ografy.tests.test_xauth',
)


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


########
# URLS #
########

ROOT_URLCONF = 'ografy.tests.urls'
