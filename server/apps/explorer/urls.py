from django.conf.urls import patterns, url

import server.apps.explorer.views as views


urlpatterns = patterns('server.apps.explorer.views',
    url(r'^(?:/(?P<search_id>[\w-]+))?/?$', views.main, name='main'),
)
