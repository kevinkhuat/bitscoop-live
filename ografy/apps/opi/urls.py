from django.conf.urls import include, patterns, url

import ografy.apps.opi.views as views


urlpatterns = patterns('',
    # Login and logout views for the browsable API
    url(r'^$', views.APIEndpoints.as_view()),
    url(r'^/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^/data/?$', views.DataView.as_view(), name='data-list'),
    url(r'^/data/(?P<pk>[a-zA-Z0-9]+)/?$', views.DataSingleView.as_view(), name='data-detail'),

    url(r'^/event/?$', views.EventView.as_view(), name='event-list'),
    url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(), name='event-detail'),

    url(r'^/location/?$', views.LocationView.as_view(), name='location-list'),

    url(r'^/message/?$', views.MessageView.as_view(), name='message-list'),
    url(r'^/message/(?P<pk>[a-zA-Z0-9]+)/?$', views.MessageSingleView.as_view(), name='message-detail'),

    url(r'^/estimate/?$', views.EstimateLocationView.as_view(), name='estimate'),

    url(r'^/permissions/?$', views.PermissionView.as_view(), name='auth-endpoint-list'),
    url(r'^/permissions/(?P<pk>[a-zA-Z0-9]+)/?$', views.PermissionSingleView.as_view(), name='auth-endpoint-detail'),

    url(r'^/play/?$', views.PlayView.as_view(), name='play-list'),
    url(r'^/play/(?P<pk>[a-zA-Z0-9]+)/?$', views.PlaySingleView.as_view(), name='play-detail'),

    url(r'^/provider/?$', views.ProviderView.as_view(), name='provider-list'),
    url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='provider-detail'),

    url(r'^/signal/?$', views.SignalView.as_view(), name='signal-list'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='signal-detail'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/provider$', views.SignalSingleView.provider, name='signal-provider'),
)
