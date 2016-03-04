from server.settings.development import *  # noqa


############
# DATABASE #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bitscoop',
        'USER': 'bitscoop_db_user',
        'PASSWORD': 'foxtrot1234',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
