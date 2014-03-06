import os


SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, '..'))

# Site setting configuration
SITE_ID = 1
ROOT_URLCONF = 'ografy.urls'
WSGI_APPLICATION = 'ografy.wsgi.application'  # Python dotted path to the WSGI application used by Django's runserver.
SECRET_KEY = '+9@@kylo*(yq-g%kx@6hhyqnenuv)$^=*!$micrn7xs_6#t7#^'
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

# Installed component configuration
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'ografy.util.middleware.MobileFlag',
    'ografy.util.middleware.XhrFlag',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    #'mptt',
    #'rest_framework',
    'tastypie',
    'tastydata',

    'ografy.apps.core',
    'ografy.apps.signals',
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

REST_FRAMEWORK = {
    'PAGINATE_BY': 15,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_msgpack.renderers.MessagePackRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework_msgpack.parsers.MessagePackParser',
        'rest_framework_csv.parsers.CSVParser',
    ),
}

SIGNALS = {
    'steam': 'http://static.ografy.io/steam.js',
    'riot': 'riot.js',
    'facebook': 'facebook.js',

    #'mycoolsite': 'https://mycoolsite.com/myapi.js'
}