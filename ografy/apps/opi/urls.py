from django.conf.urls import include, patterns, url

import ografy.apps.opi.views as views


urlpatterns = patterns('',
    # Login and logout views for the browsable API
    url(r'^$', views.APIEndpoints.as_view()),
    url(r'^/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^/contact/?$', views.ContactView.as_view(), name='contact-list'),
    url(r'^/contact/(?P<pk>[a-zA-Z0-9]+)/?$', views.ContactSingleView.as_view(), name='contact-detail'),

    url(r'^/content/?$', views.ContentView.as_view(), name='content-list'),
    url(r'^/content/(?P<pk>[a-zA-Z0-9]+)/?$', views.ContentSingleView.as_view(), name='content-detail'),

    url(r'^/event/?$', views.EventView.as_view(), name='event-list'),
    url(r'^/event/(?P<pk>[a-zA-Z0-9]+)/?$', views.EventSingleView.as_view(), name='event-detail'),

    url(r'^/location/?$', views.LocationView.as_view(), name='location-list'),

    url(r'^/provider/?$', views.ProviderView.as_view(), name='provider-list'),
    url(r'^/provider/(?P<pk>[a-zA-Z0-9]+)/?$', views.ProviderSingleView.as_view(), name='provider-detail'),

    url(r'^/estimate/?$', views.EstimateLocationView.as_view(), name='estimate'),

    url(r'^/signal/?$', views.SignalView.as_view(), name='signal-list'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/?$', views.SignalSingleView.as_view(), name='signal-detail'),
    url(r'^/signal/(?P<pk>[a-zA-Z0-9]+)/provider$', views.SignalSingleView.provider, name='signal-provider'),
)
