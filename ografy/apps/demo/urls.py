from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.demo import views


urlpatterns = patterns('',
    url(r'^/?$', views.index),
    url(r'^debug/?$', views.debug),
)
