from django.conf.urls import patterns, url

import ografy.core.views.connections as views


urlpatterns = patterns('',
    # url(r'^/?$', views.index, name='base'),
    url(r'^/authorize/?$', views.authorize, name='authorize'),
    url(r'^/authorize/(?P<pk>[0-9a-zA-Z]+)/?$', views.authorize, name='authorize_id'),
    url(r'^/connect/(?P<name>[a-zA-Z]+)/?$', views.connect, name='connect'),
    url(r'^/verify/(?P<pk>[0-9a-zA-z]+)/?$', views.verify, name='verify'),
)