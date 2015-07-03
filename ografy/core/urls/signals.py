from django.conf.urls import patterns, url

import ografy.core.views.signals as signals_views


urlpatterns = patterns('',
    url(r'^authorize/?$', signals_views.authorize, name='core_authorize'),
    url(r'^authorize/(?P<pk>[0-9a-zA-Z]+)/?$', signals_views.authorize, name='core_authorize_id'),
    url(r'^connect/?$', signals_views.providers, name='core_providers'),
    url(r'^connect/(?P<pk>[0-9a-zA-z]+)/?$', signals_views.connect, name='core_connect'),
    url(r'^connect/(?P<name>[a-zA-Z]+)/?$', signals_views.connect_name, name='core_connect_name'),
    url(r'^verify/?$', signals_views.verify, name='core_verify_base'),
    url(r'^verify/(?P<pk>[0-9a-zA-z]+)/?$', signals_views.verify, name='core_verify'),
)
