from server.settings import *  # noqa


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_path(ROOT_PATH, 'databases', 'development.db'),
    },
}


########
# HTTP #
########

ALLOWED_HOSTS = ['.bitscoop.com', 'localhost']


#############
# DEBUGGING #
#############

DEBUG = True


###########
# LOGGING #
###########

LOGGING = {}


#############
# TEMPLATES #
#############

TEMPLATE_DEBUG = True


##########
# STATIC #
##########

STATIC_URL = '/static/'
