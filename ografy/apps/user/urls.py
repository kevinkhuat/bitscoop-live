from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.user import views


urlpatterns = patterns('',
    url(r'^/(?P<oid>\w+)/?$', views.profile, name='user_profile'),
    url(r'^/?$', views.index, name='user_index'),
)
