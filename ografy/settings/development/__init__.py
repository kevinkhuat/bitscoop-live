from ografy.settings import *


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


###########
# MONGODB #
###########

MONGODB_DBNAME = 'ografy_db'
MONGODB_SERVERNAME = 'localhost'
MONGODB_SERVERPORT = 27017
