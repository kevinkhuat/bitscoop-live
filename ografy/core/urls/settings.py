from django.conf.urls import patterns, url

import ografy.core.views.settings as settings_views


urlpatterns = patterns('',
    url(r'^settings/?$', settings_views.base, name='core_settings_personal'),
    url(r'^settings/location$', settings_views.LocationView.as_view(), name='core_settings_location'),
    url(r'^settings/personal/?$', settings_views.PersonalView.as_view(), name='core_settings_personal'),
    url(r'^settings/security/?$', settings_views.SecurityView.as_view(), name='core_settings_security'),
    url(r'^settings/signals/?$', settings_views.SignalView.as_view(), name='core_settings_signals'),
    url(r'^signals/?$', settings_views.SignalView.as_view(), name='core_signals'),
)
