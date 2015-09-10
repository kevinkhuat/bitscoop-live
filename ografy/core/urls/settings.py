from django.conf.urls import patterns, url

import ografy.core.views.settings as views


urlpatterns = patterns('',
    url(r'^/?$', views.AccountView.as_view(), name='base'),
    url(r'^/account/?$', views.AccountView.as_view(), name='account'),
    url(r'^/location/?$', views.LocationView.as_view(), name='location'),
    url(r'^/security/?$', views.SecurityView.as_view(), name='security'),
    url(r'^/signals/?$', views.SignalView.as_view(), name='signals'),
)
