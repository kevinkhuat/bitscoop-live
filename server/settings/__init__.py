import re

from django.core.validators import RegexValidator

from server import ROOT_PATH, SOURCE_PATH, get_environ_setting, get_path
from server.settings.connections import *  # noqa


# Organized according to:
#     https://docs.djangoproject.com/en/1.7/ref/settings/#core-settings-topical-index


#########
# CACHE #  https://docs.djangoproject.com/en/1.7/ref/settings/#cache
#########

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer'
        },
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer'
        },
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
# CACHE_MIDDLEWARE_SECONDS = 600


############
# DATABASE #  https://docs.djangoproject.com/en/1.7/ref/settings/#database
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_path(ROOT_PATH, 'databases', 'development.db'),
    }
}
MONGODB = {
    'NAME': 'bitscoop',
    'HOST': 'localhost',
    'PORT': 27017
}
ELASTICSEARCH = {
    'HOST': 'localhost',
    'PORT': 9200,
    'USE_SSL': False
}
# DATABASE_ROUTERS = []
# DEFAULT_INDEX_TABLESPACE = ''
# DEFAULT_TABLESPACE = ''
# TRANSACTIONS_MANAGED = False


#############
# DEBUGGING #  https://docs.djangoproject.com/en/1.7/ref/settings/#debugging
#############

# DEBUG = False
# DEBUG_PROPAGATE_EXCEPTIONS = False


#########
# EMAIL #  https://docs.djangoproject.com/en/1.7/ref/settings/#email
#########

ADMINS = (
    ('Webmaster', 'webmaster+logging@bitscoop.com'),
)
# DEFAULT_CHARSET defined under "HTTP."
# DEFAULT_FROM_EMAIL = 'webmaster@localhost'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_FILE_PATH (not defined)
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_HOST_USER = ''
# EMAIL_PORT = 25
# EMAIL_SUBJECT_PREFIX = '[Django] '
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = False
# MANAGERS = ADMINS
# # SEND_BROKEN_LINK_EMAILS defined under "Error Reporting."
# SERVER_EMAIL = 'root@localhost'


###################
# ERROR REPORTING #  https://docs.djangoproject.com/en/1.7/ref/settings/#error-reporting
###################

# DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'
# IGNORABLE_404_URLS = ()
# MANAGERS defined under email.
# SEND_BROKEN_LINK_EMAILS = False
# SILENCED_SYSTEM_CHECKS = []


################
# FILE UPLOADS #  https://docs.djangoproject.com/en/1.7/ref/settings/#file-uploads
################

# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# FILE_CHARSET = 'utf-8'
# FILE_UPLOAD_HANDLERS = (
#     'django.core.files.uploadhandler.MemoryFileUploadHandler',
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
# )
# FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
# FILE_UPLOAD_PERMISSIONS = None
# FILE_UPLOAD_TEMP_DIR = None
# MEDIA_ROOT = ''
# MEDIA_URL = ''


#################
# GLOBALIZATION #  https://docs.djangoproject.com/en/1.7/ref/settings/#globalization-i18n-l10n
#################

# DATE_FORMAT = 'N j, Y'
# DATE_INPUT_FORMATS = (
#     '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
#     '%b %d %Y', '%b %d, %Y',             # 'Oct 25 2006', 'Oct 25, 2006'
#     '%d %b %Y', '%d %b, %Y',             # '25 Oct 2006', '25 Oct, 2006'
#     '%B %d %Y', '%B %d, %Y',             # 'October 25 2006', 'October 25, 2006'
#     '%d %B %Y', '%d %B, %Y',             # '25 October 2006', '25 October, 2006'
# )
# DATETIME_FORMAT = 'N j, Y, P'
# DATETIME_INPUT_FORMATS = (
#     '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
#     '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
#     '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
#     '%Y-%m-%d',              # '2006-10-25'
#     '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
#     '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
#     '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
#     '%m/%d/%Y',              # '10/25/2006'
#     '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
#     '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
#     '%m/%d/%y %H:%M',        # '10/25/06 14:30'
#     '%m/%d/%y',              # '10/25/06'
# )
# DECIMAL_SEPARATOR = '.'
# FIRST_DAY_OF_WEEK = 0
# FORMAT_MODULE_PATH = None
# LANGUAGE_CODE = 'en-us'
# LANGUAGE_COOKIE_AGE = None
# LANGUAGE_COOKIE_DOMAIN = None
# LANGUAGE_COOKIE_NAME = 'django_language'
# LANGUAGE_COOKIE_PATH = '/'
# LANGUAGES = (
#     # ... Lots of default stuff ...
# )
# LOCALE_PATHS = ()
# MONTH_DAY_FORMAT = 'F j'
# NUMBER_GROUPING = 0
# SHORT_DATE_FORMAT = 'm/d/Y'
# SHORT_DATETIME_FORMAT = 'm/d/Y P'
# THOUSAND_SEPARATOR = ','
# TIME_FORMAT = 'P'
# TIME_INPUT_FORMATS = (
#     '%H:%M:%S',     # '14:30:59'
#     '%H:%M:%S.%f',  # '14:30:59.000200'
#     '%H:%M',        # '14:30'
# )
TIME_ZONE = 'America/New_York'
# USE_I18N = True
USE_L10N = True
# USE_THOUSAND_SEPARATOR = False
USE_TZ = True
# YEAR_MONTH_FORMAT = 'F Y'


########
# HTTP #  https://docs.djangoproject.com/en/1.7/ref/settings/#http
########

ALLOWED_HOSTS = ['.bitscoop.com']
# DEFAULT_CHARSET = 'utf-8'
# DEFAULT_CONTENT_TYPE = 'text/html'
# DISALLOWED_USER_AGENTS = ()
# FORCE_SCRIPT_NAME = None
# INTERNAL_IPS = ()
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'server.contrib.pytoolbox.django.middleware.AcceptMiddleware',  # Parses HTTP-Accept headers.
    'server.contrib.multiauth.plugins.session.middleware.IpMiddleware',  # Sets the IP address on the request.
    'server.contrib.pytoolbox.django.middleware.SetAnonymousTestCookie',  # Set test cookie for anonymous users.
)

# SECURE_PROXY_SSL_HEADER = None
# SIGNING_BACKEND = 'django.core.signing.TimestampSigner'
# USE_ETAGS = False
# USE_X_FORWARDED_HOST = False
WSGI_APPLICATION = 'wsgi.application'


###########
# LOGGING #  https://docs.djangoproject.com/en/1.7/ref/settings/#id8
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/bitscoop/debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# LOGGING_CONFIG = 'logging.config.dictConfig'


##########
# MODELS #  https://docs.djangoproject.com/en/1.7/ref/settings/#models
##########

# ABSOLUTE_URL_OVERRIDES = {}
FIXTURE_DIRS = (
    get_path(ROOT_PATH, 'fixtures'),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rest_framework',
    'social.apps.django_app.default',

    'server.apps.opi',
    'server.contrib.multiauth',
    'server.core',
)


############
# SECURITY #  https://docs.djangoproject.com/en/1.7/ref/settings/#security
############

# CSRF_COOKIE_DOMAIN = None
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_NAME = 'csrftoken'
# CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_AGE = 60 * 60 * 24 * 7 * 52
CSRF_FAILURE_VIEW = 'server.core.views.errors.view403'
# FIXME: Should we be version controlling this? Where does this setting manifest other than signed cookie sessions (which we aren't using)?
SECRET_KEY = '~-/W,dd1~t|"#%Y#pIag%28ua1wmKWclQ<ntDQxD)X~_S9bSa?Z/9K[(g?0u1LglbA86?qqW,B5GiaFN'
# X_FRAME_OPTIONS = 'SAMEORIGIN'


#################
# SERIALIZATION #  https://docs.djangoproject.com/en/1.7/ref/settings/#serialization
#################

# DEFAULT_CHARSET Defined under HTTP.
# SERIALIZATION_MODULES not defined.


#############
# TEMPLATES #  https://docs.djangoproject.com/en/1.7/ref/settings/#templates
#############

# ALLOWED_INCLUDE_ROOTS = ()
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',

    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',

    'server.contrib.pytoolbox.django.context_processors.page_name',
)
# TEMPLATE_DEBUG = False
TEMPLATE_DIRS = (
    get_path(ROOT_PATH, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
# TEMPLATE_STRING_IF_INVALID = ''


###########
# TESTING #  https://docs.djangoproject.com/en/1.7/ref/settings/#testing
###########

# TEST_NON_SERIALIZED_APPS = []
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'


########
# URLS #  https://docs.djangoproject.com/en/1.7/ref/settings/#urls
########

APPEND_SLASH = False
# PREPEND_WWW = False
ROOT_URLCONF = 'server.urls'


########
# AUTH #  https://docs.djangoproject.com/en/1.7/ref/settings/#auth
########

# FIXME: Temporarily moved AUTHENTICATION_BACKENDS setting to server.settings.signals. Look for a cleaner way to separate application authentication and signal association.
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
# )
AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = ''
LOGIN_URL = '/login'
# LOGOUT_URL = '/accounts/logout/'
# PASSWORD_RESET_TIMEOUT_DAYS = 3
PASSWORD_HASHERS = (
    # 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


############
# SESSIONS #  https://docs.djangoproject.com/en/1.7/ref/settings/#sessions
############

SESSION_CACHE_ALIAS = 'session'
# SESSION_COOKIE_NAME = 'sessionid'
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_COOKIE_DOMAIN = '.bitscoop.com'
SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_PATH = '/'
# SESSION_COOKIE_HTTPONLY = True
# SESSION_SAVE_EVERY_REQUEST = False
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_FILE_PATH = None
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


##########
# STATIC #  https://docs.djangoproject.com/en/1.7/ref/settings/#static-files
##########

STATIC_ROOT = get_path(ROOT_PATH, 'build', 'static')
STATIC_URL = get_environ_setting('STATIC_URL', '/static/')
STATICFILES_DIRS = (
    get_path(ROOT_PATH, 'artifacts'),
)
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )


##################
# REST FRAMEWORK #  https://http://www.django-rest-framework.org/
##################

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'server.core.pagination.TwentyItemPageView',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DATETIME_FORMAT': 'iso-8601',
    'DATETIME_INPUT_FORMATS': ['iso-8601']
    # 'PAGINATE_BY': 2
}


########
# CORE #
########

HANDLE_VALIDATORS = [
    RegexValidator(re.compile(r'^(?=[a-zA-Z0-9_\.]{3,20}$)(?=.*[a-zA-Z])'), '3-20 letters, numbers, underscores, or periods. Must contain at least one letter.'),
    RegexValidator(re.compile(r'[b]+[i1\|]+[t7]+[s5]+[c]+[o0]+[p]*', re.I), 'Username cannot contain BitScoop.', inverse_match=True),
]
INVALID_PASSWORD_MESSAGE = '8-48 characters. At least one lowercase, one uppercase, and one number.'
PASSWORD_REGEXP = r'^(?=.{8,48}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*'


#############
# MULTIAUTH #
#############

MULTIAUTH_AUTH_ERROR = 'django.http.Http404'
MULTIAUTH_HASH_MINLENGTH = 5
MULTIAUTH_HASH_SECRET = '65-va3nry3g0z_937wguu0$5yyz)*(ko)v7)$letyq%&hii!8u'
