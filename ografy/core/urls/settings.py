from django.conf.urls import patterns, url

import ografy.core.views.settings as settings_views


urlpatterns = patterns('',
    url(r'^/?$', settings_views.AccountView.as_view(), name='core_settings_account'),
    url(r'^account/?$', settings_views.AccountView.as_view(), name='core_settings_account'),
    url(r'^location/?$', settings_views.LocationView.as_view(), name='core_settings_location'),
    url(r'^security/?$', settings_views.SecurityView.as_view(), name='core_settings_security'),
    url(r'^signals/?$', settings_views.SignalView.as_view(), name='core_settings_signals'),
)
