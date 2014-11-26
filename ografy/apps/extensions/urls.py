from django.conf.urls import patterns, url

from ografy.apps.extensions import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='extensions_index'),
)
