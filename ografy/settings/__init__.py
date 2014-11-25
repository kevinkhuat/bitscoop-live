import os

from ografy.settings.signals import *


# Organized according to:
#     https://docs.djangoproject.com/en/1.7/ref/settings/#core-settings-topical-index


SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, '..'))


#########
# CACHE #  https://docs.djangoproject.com/en/1.7/ref/settings/#cache
#########

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
# CACHE_MIDDLEWARE_SECONDS = 600


############
# DATABASE #  https://docs.djangoproject.com/en/1.7/ref/settings/#database
############

# DATABASES = {}
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
    ('Webmaster', 'webmaster+logging@ografy.io'),
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

ALLOWED_HOSTS = ['.ografy.io']
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

    'ografy.util.middleware.SetMobileFlag',  # Set Mobile request yes/no flag for all requests.
    'ografy.util.middleware.SetXhrFlag',  # Set XMLHttpRequest yes/no flag for all requests.
    'ografy.util.middleware.SetAnonymousTestCookie',  # Set test cookie for anonymous users.
)
# SECURE_PROXY_SSL_HEADER = None
# SIGNING_BACKEND = 'django.core.signing.TimestampSigner'
# USE_ETAGS = False
# USE_X_FORWARDED_HOST = False
WSGI_APPLICATION = 'ografy.wsgi.application'


###########
# LOGGING #  https://docs.djangoproject.com/en/1.7/ref/settings/#id8
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.abspath(os.path.join(ROOT_PATH, '..', 'logs', 'debug.log')),
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
   os.path.abspath(os.path.join(ROOT_PATH, 'ografy', 'apps', 'xauth', 'fixtures')),
)
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',

    'ografy.apps.account',
    'ografy.apps.xauth',
    #'ografy.apps.api',
    'ografy.apps.blog',
    'ografy.apps.core',
    'ografy.apps.demo',
    'ografy.apps.documentation',
    #'ografy.apps.extensions',
    #'ografy.apps.nexus',
    #'ografy.apps.signals',
    'ografy.apps.user',

    'ografy.tests.test_obase',
    'ografy.tests.test_xauth',
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
# CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
SECRET_KEY = '~-/W,dd1~t|"#%Y#pIag%28ua1wmKWclQ<ntDQxD)X~_S9bSa?Z/9K[(g?0u1LglbA86?qqW,B5GiaFN'  # TODO: Make this actually secure and don't version control it.
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
)
# TEMPLATE_DEBUG = False
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(ROOT_PATH, 'templates')),
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
ROOT_URLCONF = 'ografy.urls'


########
# AUTH #  https://docs.djangoproject.com/en/1.7/ref/settings/#auth
########

AUTHENTICATION_BACKENDS = (
    'social.backends.amazon.AmazonOAuth2',
    'social.backends.angel.AngelOAuth2',
    'social.backends.aol.AOLOpenId',
    'social.backends.appsfuel.AppsfuelOAuth2',
    'social.backends.beats.BeatsOAuth2',
    'social.backends.behance.BehanceOAuth2',
    'social.backends.belgiumeid.BelgiumEIDOpenId',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.box.BoxOAuth2',
    'social.backends.clef.ClefOAuth2',
    'social.backends.coinbase.CoinbaseOAuth2',
    'social.backends.dailymotion.DailymotionOAuth2',
    'social.backends.disqus.DisqusOAuth2',
    'social.backends.douban.DoubanOAuth2',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.dropbox.DropboxOAuth2',
    'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.fedora.FedoraOpenId',
    'social.backends.fitbit.FitbitOAuth',
    'social.backends.flickr.FlickrOAuth',
    'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.google.GoogleOpenIdConnect',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.jawbone.JawboneOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.live.LiveOAuth2',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.mailru.MailruOAuth2',
    'social.backends.mendeley.MendeleyOAuth',
    'social.backends.mendeley.MendeleyOAuth2',
    'social.backends.mixcloud.MixcloudOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.orkut.OrkutOAuth',
    'social.backends.persona.PersonaAuth',
    'social.backends.podio.PodioOAuth2',
    'social.backends.rdio.RdioOAuth1',
    'social.backends.rdio.RdioOAuth2',
    'social.backends.readability.ReadabilityOAuth',
    'social.backends.reddit.RedditOAuth2',
    'social.backends.runkeeper.RunKeeperOAuth2',
    'social.backends.skyrock.SkyrockOAuth',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.spotify.SpotifyOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    'social.backends.steam.SteamOpenId',
    'social.backends.stocktwits.StocktwitsOAuth2',
    'social.backends.stripe.StripeOAuth2',
    'social.backends.suse.OpenSUSEOpenId',
    'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social.backends.trello.TrelloOAuth',
    'social.backends.tripit.TripItOAuth',
    'social.backends.tumblr.TumblrOAuth',
    'social.backends.twilio.TwilioAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.vk.VKOAuth2',
    'social.backends.weibo.WeiboOAuth2',
    'social.backends.xing.XingOAuth',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.yammer.YammerOAuth2',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.vimeo.VimeoOAuth1',
    'social.backends.lastfm.LastFmAuth',
    'social.backends.moves.MovesOAuth2',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
    'ografy.apps.xauth.backends.IdentifierBackend',
    'ografy.apps.xauth.backends.DummyTokenBackend',
)
AUTH_USER_MODEL = 'xauth.User'
# LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_URL = '/auth/applogin/'
# LOGOUT_URL = '/accounts/logout/'
# PASSWORD_RESET_TIMEOUT_DAYS = 3
PASSWORD_HASHERS = (
    #'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    #'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


############
# SESSIONS #  https://docs.djangoproject.com/en/1.7/ref/settings/#sessions
############

# SESSION_CACHE_ALIAS = 'default'
# SESSION_COOKIE_NAME = 'sessionid'
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_PATH = '/'
# SESSION_COOKIE_HTTPONLY = True
# SESSION_SAVE_EVERY_REQUEST = False
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_FILE_PATH = None
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


##########
# STATIC #  https://docs.djangoproject.com/en/1.7/ref/settings/#static-files
##########

STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'build', 'static'))
STATIC_URL = 'https://static.ografy.io/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(ROOT_PATH, 'static')),
)
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )


#########
# XAUTH #
#########

PASSWORD_REGEXP = r'^(?=.{8,48}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*'
INVALID_PASSWORD_MESSAGE = '8-48 characters. At least one lowercase, one uppercase, and one number.'
