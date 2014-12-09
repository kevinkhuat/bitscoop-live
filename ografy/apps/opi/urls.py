from django.conf.urls import patterns, url
from django.conf.urls import include

import ografy.apps.opi.views as views


# API endpoints
provider_list = views.ProviderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
provider_detail = views.ProviderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
signal_list = views.SignalViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
signal_detail = views.SignalViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
signal_provider = views.SignalViewSet.as_view({
    'get': 'provider'
})
user_list = views.UserViewSet.as_view({
    'get': 'list'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = patterns('',
   # Login and logout views for the browsable API
   url(r'^$', views.APIListView.as_view()),

   url(r'^/data/?$', views.DataView.as_view(), name='data-list'),
   url(r'^/data/(?P<pk>[a-zA-Z0-9]+)/?$', views.DataSingleView.as_view(), name='data-detail'),
   url(r'^/event/?$', views.EventView.as_view(), name='event-list'),
   url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(), name='event-detail'),
   url(r'^/message/?$', views.MessageView.as_view(), name='message-list'),
   url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/?$', views.MessageSingleView.as_view(), name='message-detail'),
   url(r'^/settings/?$', views.SettingsView.as_view(), name='settings-list'),
   url(r'^/settings/(?P<pk>[a-zA-Z0-9]+)/?$', views.SettingsSingleView.as_view(), name='settings-detail'),

   url(r'^/provider$', provider_list, name='provider-list'),
   url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', provider_detail, name='provider-detail'),
   url(r'^/signal$', signal_list, name='signal-list'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', signal_detail, name='signal-detail'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)', signal_provider, name='signal-provider'),
   url(r'^/user$', user_list, name='user-list'),
   url(r'^/user/(?P<pk>[a-zA-Z0-9]+)', user_detail, name='user-detail'),
   url(r'^/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
