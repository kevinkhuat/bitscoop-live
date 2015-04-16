from django.conf.urls import patterns, url

import ografy.apps.core.views as views
import ografy.apps.core.views.main as main_views
import ografy.apps.core.views.settings as settings_views
import ografy.apps.core.views.signals as signals_views
import ografy.apps.core.views.user as user_views
import ografy.apps.core.views.search as search_views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),

    #TODO: Make this general to any key we need to get, not hard-coded to Mapbox's token
    url(r'^app/keys/mapbox?$', main_views.mapbox_token, name='mapbox_token'),

    url(r'^settings/?$', settings_views.base, name='core_settings_personal'),
    url(r'^settings/personal/?$', settings_views.PersonalView.as_view(), name='core_settings_personal'),
    url(r'^settings/security/?$', settings_views.SecurityView.as_view(), name='core_settings_security'),
    url(r'^settings/signals/?$', settings_views.SignalView.as_view(), name='core_settings_signals'),

    url(r'^user/?$', user_views.my_profile, name='core_user_my_profile'),
    url(r'^user/(?P<handle>\w+)/?$', user_views.profile, name='core_user_profile'),
    # FIXME: Adjust names of these urls, should they be user URLs, or core URLs?
    url(r'^signals/?$', settings_views.SignalView.as_view(), name='core_signals'),
    url(r'^signals/(?P<pk>[a-zA-Z0-9]+)/?$', user_views.signals, name='core_signals'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),

    url(r'^authorize/?$', signals_views.authorize, name='core_authorize'),
    url(r'^authorize/(?P<pk>[0-9]+)/?$', signals_views.authorize, name='core_authorize_id'),
    url(r'^connect/?$', signals_views.providers, name='core_providers'),
    url(r'^connect/(?P<pk>[0-9]+)/?$', signals_views.connect, name='core_connect'),
    url(r'^connect/(?P<name>[a-zA-Z]+)/?$', signals_views.connect_name, name='core_connect_name'),
    url(r'^verify/(?P<pk>[0-9]+)/?$', signals_views.verify, name='core_verify'),

    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),

    url(r'^search/event$', search_views.SearchView.as_view(), name='search_event'),
)
