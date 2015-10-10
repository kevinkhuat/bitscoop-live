from django.conf.urls import patterns, url

import ografy.apps.explorer.views as views


urlpatterns = patterns('ografy.apps.explorer.views',
    url(r'^/?$', views.main, name='main'),
)
