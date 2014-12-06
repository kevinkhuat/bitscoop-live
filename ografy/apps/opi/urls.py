from django.conf.urls import patterns, url

import ografy.apps.opi.views as views


urlpatterns = patterns('',
    url(r'^/data/?$', views.DataView.as_view(), name='opi_data'),
    url(r'^/data/(?P<id>[a-zA-Z0-9]+)/?$', views.DataSingleView.as_view(), name='opi_data_single'),
    url(r'^/event/?$', views.EventView.as_view(), name='opi_event'),
    url(r'^/event/(?P<id>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(), name='opi_event_single'),
    url(r'^/message/?$', views.MessageView.as_view(), name='opi_message'),
    url(r'^/message/(?P<id>[a-zA-Z0-9]+)/?$', views.MessageSingleView.as_view(), name='opi_message_single'),
    url(r'^/provider/?$', views.ProviderView.as_view(), name='opi_provider'),
    url(r'^/provider/(?P<id>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='opi_provider_single'),
    url(r'^/settings/?$', views.SettingsView.as_view(), name='opi_settings'),
    url(r'^/signal/?$', views.SignalView.as_view(), name='opi_signal'),
    url(r'^/signal/(?P<id>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='opi_signal_single'),
    url(r'^/user/?$', views.UserView.as_view(), name='opi_user'),
    url(r'^/user/(?P<id>[a-zA-Z0-9]+)/?$', views.UserSingleView.as_view(), name='opi_user_single'),
)
