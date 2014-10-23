from __future__ import unicode_literals

import os


SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SETTINGS_PATH, '..'))

# Site setting configuration
ROOT_URLCONF = 'ografy.urls'
APPEND_SLASH = False
WSGI_APPLICATION = 'ografy.wsgi.application'  # Python dotted path to the WSGI application used by Django's runserver.
SECRET_KEY = '~-/W,dd1~t|"#%Y#pIag%28ua1wmKWclQ<ntDQxD)X~_S9bSa?Z/9K[(g?0u1LglbA86?qqW,B5GiaFN'  # TODO: Make this actually secure and don't version control it.
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
AUTH_USER_MODEL = 'xauth.User'
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
LOGIN_URL = '/auth/applogin/'
PASSWORD_HASHERS = (
    # TODO: Move bcrypt up when not on Dreamhost.
    # 'django.contrib.xauth.hashers.BCryptSHA256PasswordHasher',
    # 'django.contrib.xauth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
SESSION_LIMIT = 1209600  # Session limit in seconds. Can also use timedelta.
RESERVED_HANDLES = {
    'blog',
    'login',
    'logout',
    'nexus',
    'settings',
    'user',
}
PASSWORD_REGEXP = r'^(?=.{8,48}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*'
INVALID_PASSWORD_MESSAGE = '8-48 characters. At least one lowercase, one uppercase, and one number.'


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

    'ografy.tests.xauth',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
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

FIXTURE_DIRS = (
   '/ografy/apps/xauth/fixtures',
)