from ografy.settings import *


##########
# MODELS #  https://docs.djangoproject.com/en/1.7/ref/settings/#models
##########

# ABSOLUTE_URL_OVERRIDES = {}
FIXTURE_DIRS = (
   os.path.abspath(os.path.join(ROOT_PATH, 'ografy', 'apps', 'xauth', 'fixtures')),
)
INSTALLED_APPS += (
    'ografy.tests.test_obase',
    'ografy.tests.test_xauth',
)


########
# URLS #  https://docs.djangoproject.com/en/1.7/ref/settings/#urls
########

APPEND_SLASH = False
# PREPEND_WWW = False
ROOT_URLCONF = 'ografy.test_urls'
