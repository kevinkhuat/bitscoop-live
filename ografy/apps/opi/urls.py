from django.conf.urls import patterns, url

import ografy.apps.opi.views as views


urlpatterns = patterns('',

    url(r'^/provider/?$', views.ProviderView.as_view(), name='provider-list'),
    url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='provider-detail'),

    url(r'^/signal/?$', views.SignalView.as_view(), name='signal-list'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='signal-detail'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/provider$', views.SignalSingleView.provider, name='signal-provider'),
)
