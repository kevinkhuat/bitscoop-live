from django.conf.urls import patterns, url

import ografy.apps.auth.views as views


urlpatterns = patterns('',
    url(r'^$', views.home, name='allauth_home'),
    url(r'^done/$', views.done, name='allauth_done'),
    url(r'^email/$', views.require_email, name='allauth_require_email'),
    url(r'^email-sent/', views.validation_sent, name='allauth_validation_sent'),
    url(r'^login/$', views.home, name='allauth_login'),
    url(r'^logout/$', views.logout, name='allauth_logout')
)
