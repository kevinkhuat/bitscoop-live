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
MONGODB = {
    'NAME': 'ografy_db',
    'HOST': 'localhost',
    'PORT': 27017,
    # 'SSL_CERT_FILE': 'PLACEHOLDER',
    # 'SSL_CERT_REQS': ssl.CERT_REQUIRED,
    # 'SSL_CA_CERTS': 'PLACEHOLDER',
}
