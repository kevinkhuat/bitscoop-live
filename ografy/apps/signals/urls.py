from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.signals import views

urlpatterns = patterns('',
    url(r'^/?$', views.index, name='signals_index')
)
