from ografy.settings.development import *


# Site setting configuration
ROOT_URLCONF = 'admin.urls'
WSGI_APPLICATION = 'admin.wsgi.application'  # Python dotted path to the WSGI application used by Django's runserver.

# Authentication
AUTH_USER_MODEL = 'xauth.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Installed component configuration
INSTALLED_APPS += ('django.contrib.admin', 'admin.apps.ografy',)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)
