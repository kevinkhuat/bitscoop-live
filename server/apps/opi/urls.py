from django.conf.urls import patterns, url

import server.apps.opi.views as views


urlpatterns = patterns('',

    url(r'^/providers/?$', views.ProviderView.as_view(), name='provider-list'),
    url(r'^/providers/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='provider-detail'),

    url(r'^/connections/?$', views.ConnectionView.as_view(), name='connection-list'),
    url(r'^/connections/(?P<pk>[a-zA-Z0-9]+)/?$', views.ConnectionSingleView.as_view(), name='connection-detail'),
    url(r'^/connections/(?P<pk>[a-zA-Z0-9]+)/provider$', views.ConnectionSingleView.provider, name='connection-provider'),
)
