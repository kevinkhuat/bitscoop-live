from ografy.settings import *  # noqa


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

ALLOWED_HOSTS = ['.ografy.io', 'localhost']


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
