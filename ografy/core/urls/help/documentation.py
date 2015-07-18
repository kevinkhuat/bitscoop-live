from django.conf.urls import patterns, url

import ografy.core.views.help.documentation as documentation_views


urlpatterns = patterns('',
    url(r'^account/?$', documentation_views.account_creation, name='help_account_creation'),
    url(r'^association/?$', documentation_views.signal_association, name='help_signal_association'),
    url(r'^main/?$', documentation_views.main_app, name='help_main_app'),
    url(r'^settings/?$', documentation_views.settings, name='help_settings'),
    url(r'^pinhomepage/?$', documentation_views.pin_to_homepage, name='help_pin_to_homepage'),
    url(r'^password/?$', documentation_views.password, name='help_password'),
)
