from django.conf.urls import patterns, url, include

import ografy.tests.xauth.views as views


urlpatterns = patterns('',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.home, name='test_xauth_home'),
    url(r'^done/$', views.done, name='test_xauth_done'),
    url(r'^email/$', views.require_email, name='test_xauth_require_email'),
    url(r'^email-sent/', views.validation_sent, name='test_xauth_validation_sent'),
    url(r'^login/$', views.home, name='test_xauth_login'),
    url(r'^logout/$', views.logout, name='test_xauth_logout')
)
