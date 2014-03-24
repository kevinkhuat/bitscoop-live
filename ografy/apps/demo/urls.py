from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.demo import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='demo_index'),
    url(r'^/dashboard/?$', views.dashboard, name='demo_dashboard'),
    url(r'^/info/?$', views.info, name='demo_info'),
    url(r'^/plan/?$', views.plan, name='demo_plan'),
)
