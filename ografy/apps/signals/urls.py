from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.signals import views

urlpatterns = patterns('',
    url(r'^/?$', views.index, name='signals_index'),
    url(r'^/get/?$', views.server_get, name='server_get'),
    url(r'^/facebook/?$', views.signal_facebook, name='signals_facebook'),
    url(r'^/twitter/?$', views.signal_twitter, name='signals_twitter'),
    url(r'^/steam/?$', views.signal_steam, name='signals_steam')
)

