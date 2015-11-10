from django.conf.urls import patterns, url

import server.core.views.connections as views


urlpatterns = patterns('',
    # url(r'^/?$', views.index, name='base'),
    url(r'^/authorize/?$', views.AuthorizeView.as_view(), name='authorize'),
    url(r'^/authorize/(?P<pk>[0-9a-zA-Z]+)/?$', views.AuthorizeView.as_view(), name='authorize_id'),
    url(r'^/connect/(?P<name>[a-zA-Z]+)/?$', views.ConnectView.as_view(), name='connect'),
)
