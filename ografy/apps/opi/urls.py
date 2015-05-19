from django.conf.urls import patterns, url
from django.conf.urls import include

import ografy.apps.opi.views as views

urlpatterns = patterns('',
   # Login and logout views for the browsable API
   url(r'^$', views.APIEndpoints.as_view()),
   url(r'^/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   url(r'^/data$', views.DataView.as_view(), name='data-list'),
   url(r'^/data/(?P<pk>[a-zA-Z0-9]+)/?$', views.DataSingleView.as_view(), name='data-detail'),

   url(r'^/event$', views.EventView.as_view(), name='event-list'),
   url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(), name='event-detail'),
   url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/data$', views.EventSingleView.data, name='event-detail'),

   url(r'^/message$', views.MessageView.as_view(), name='message-list'),
   url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/?$', views.MessageSingleView.as_view(), name='message-detail'),
   url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/event$', views.MessageSingleView.event, name='message-detail'),
   url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/event/data$', views.MessageSingleView.data, name='message-detail'),

   url(r'^/authorized_endpoints$', views.AuthorizedEndpointView.as_view(), name='auth-endpoint-list'),
   url(r'^/authorized_endpoints/(?P<pk>[a-zA-Z0-9]+)/?$', views.AuthorizedEndpointSingleView.as_view(), name='auth-endpoint-detail'),

   url(r'^/play$', views.PlayView.as_view(), name='play-list'),
   url(r'^/play/(?P<pk>[a-zA-Z0-9]+)/?$', views.PlaySingleView.as_view(), name='play-detail'),
   url(r'^/play/(?P<pk>[a-zA-Z0-9]+)/event$', views.PlaySingleView.event, name='play-detail'),
   url(r'^/play/(?P<pk>[a-zA-Z0-9]+)/event/data$', views.PlaySingleView.data, name='play-detail'),

   url(r'^/provider$', views.ProviderView.as_view(), name='provider-list'),
   url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='provider-detail'),

   url(r'^/signal$', views.SignalView.as_view(), name='signal-list'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='signal-detail'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/provider$', views.SignalSingleView.provider, name='signal-provider'),

   url(r'^/settings$', views.SettingsView.as_view(), name='settings-list'),
   url(r'^/settings/(?P<pk>[a-zA-Z0-9]+)/?$', views.SettingsSingleView.as_view(), name='settings-detail'),

   url(r'^/user$', views.UserView.as_view(), name='user-list'),
   url(r'^/user/(?P<pk>[a-zA-Z0-9]+)', views.UserSingleView.as_view(), name='user-detail'),
)
