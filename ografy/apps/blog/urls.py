from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.blog import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='blog_index'),
    url(r'^/(?P<slug>[^/]+)/?$', views.post, name='blog_post'),
)
