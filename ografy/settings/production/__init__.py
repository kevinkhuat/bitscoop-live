from ografy.settings import *


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ografy_db',
        'USER': 'ografy_db_user',
        'PASSWORD': 'foxtrot1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


###########
# MONGODB #
###########

MONGODB_DBNAME = 'ografy_db'
MONGODB_SERVERNAME = 'localhost'
MONGODB_SERVERPORT = 27017


#############
# TEMPLATES #
#############

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
