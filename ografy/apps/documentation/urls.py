from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.documentation import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='documentation_index'),
)
