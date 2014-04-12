from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ografy.apps.account import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='account_index'),
    url(r'/details/?$', views.DetailsView.as_view(), name='account_details'),
    url(r'/password/?$', views.PasswordView.as_view(), name='account_password'),
)
