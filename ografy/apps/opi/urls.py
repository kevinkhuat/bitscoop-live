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
   url(r'^/data/?$', views.DataView.as_view(), name='opi_data'),
   url(r'^/data/(?P<pk>[a-zA-Z0-9]+)/?$', views.DataSingleView.as_view(), name='opi_data_single'),
   url(r'^/event/?$', views.EventView.as_view(), name='opi_event'),
   url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(),
       name='opi_event_single'),
   url(r'^/message/?$', views.MessageView.as_view(), name='opi_message'),
   url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/?$', views.MessageSingleView.as_view(),
       name='opi_message_single'),

   # Login and logout views for the browsable API
   url(r'^$', views.APIListView.as_view()),
   url(r'^/provider$', provider_list, name='provider-list'),
   url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', provider_detail, name='provider-detail'),
   url(r'^/signal$', signal_list, name='signal-list'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', signal_detail, name='signal-detail'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)', signal_provider, name='signal-provider'),
   url(r'^/user$', user_list, name='user-list'),
   url(r'^/user/(?P<pk>[a-zA-Z0-9]+)', user_detail, name='user-detail'),
   url(r'^/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   # url(r'^/provider/?$', views.ProviderView.as_view(), name='opi_provider'),
   # url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='opi_provider_single'),
   # url(r'^/settings/?$', views.SettingsView.as_view(), name='opi_settings'),
   # url(r'^/signal/?$', views.SignalView.as_view(), name='opi_signal'),
   # url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='opi_signal_single'),
   # url(r'^/user/?$', views.UserView.as_view(), name='opi_user'),
   # url(r'^/user/(?P<pk>[a-zA-Z0-9]+)/?$', views.UserSingleView.as_view(), name='opi_user_single'),
)
