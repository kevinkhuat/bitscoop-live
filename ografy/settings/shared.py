import os


SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, '..'))

# Site setting configuration
ROOT_URLCONF = 'ografy.urls'
APPEND_SLASH = False
WSGI_APPLICATION = 'ografy.wsgi.application'  # Python dotted path to the WSGI application used by Django's runserver.
SECRET_KEY = '+9@@kylo*(yq-g%kx@6hhyqnenuv)$^=*!$micrn7xs_6#t7#^'  # TODO: Make this actually secure and don't version control it.
ADMINS = (
    ('Steven Berry', 'sberry@ografy.io'),
    ('Liam Broza', 'lbroza@ografy.io'),
)
MANAGERS = ADMINS

# Localization configuration
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True  # Load the internationalization machinery.
USE_L10N = True  # Format dates, numbers and calendars according to current locale.
# DATETIME_FORMAT = 'Y/m/d'  # Use if not using L10N
# DATE_FORMAT = 'Y/m/d'  # Use if not using L10N
USE_TZ = True  # Use timezone-aware datetimes.

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(ROOT_PATH, '..', 'databases', 'data.db')),
    },
}

# Authentication
AUTH_USER_MODEL = 'core.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

    'ografy.lib.auth.backends.DummyTokenBackend',
)
LOGIN_URL = '/login/'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
SESSION_LIMIT = 1209600  # Session limit in seconds. Can also use timedelta.


# Installed component configuration
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'ografy.util.middleware.SetMobileFlag',  # Set Mobile request yes/no flag for all requests.
    'ografy.util.middleware.SetXhrFlag',  # Set XMLHttpRequest yes/no flag for all requests.
    'ografy.util.middleware.SetAnonymousTestCookie',  # Set test cookie for anonymous users.
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'mptt',
    #'rest_framework',
    'smokesignal',
    'tastypie',
    'tastydata',

    'ografy.apps.api',
    'ografy.apps.blog',
    'ografy.apps.core',
    'ografy.apps.demo',
    'ografy.apps.documentation',
    'ografy.apps.signals',

    'ografy.lib.auth',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

# Template configuration
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(ROOT_PATH, 'templates')),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Static file configuration
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(ROOT_PATH, 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'build', 'static'))


# Contrib Settings
TASTYDATA_PAGE_LIMIT = 30

SIGNALS = {
    'steam': 'http://static.ografy.io/steam.js',
    'riot': 'riot.js',
    'facebook': 'facebook.js',

    #'mycoolsite': 'https://mycoolsite.com/myapi.js',
}
