from django.conf.urls import url, patterns
from rest_framework.urlpatterns import format_suffix_patterns

from ografy.apps.api import views

provider_list = views.ProviderViewSet.as_view({
    'get': 'list',
})

provider_detail = views.ProviderViewSet.as_view({
    'get': 'retrieve'
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

urlpatterns = patterns('',
   url(r'^$', views.api_root),
)

urlpatterns += format_suffix_patterns([
   url(r'^/provider$', provider_list, name='api-provider-list'),
   url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', provider_detail, name='api-provider-detail'),

   url(r'^/signal$', signal_list, name='api-signal-list'),
   url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', signal_detail, name='api-signal-detail'),
], allowed=['json', 'html'])
