from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ografy.apps.api import views


urlpatterns = format_suffix_patterns(patterns('',
    url(r'^/?$', views.RootIndex.as_view(), name = 'api-root'),
    url(r'^/users/?$', views.UserList.as_view(), name = 'user-list'),
    url(r'^/users/(?P<pk>[0-9]+)/?$', views.UserDetail.as_view(), name = 'user-detail'),
    url(r'^/accounts/?$', views.AccountList.as_view(), name = 'account-list'),
    url(r'^/accounts/(?P<pk>[0-9]+)/?$', views.AccountDetail.as_view(), name = 'account-detail'),
    url(r'^/entries/?$', views.EntryList.as_view(), name = 'entry-list'),
    url(r'^/entries/(?P<pk>[0-9]+)/?$', views.EntryDetail.as_view(), name = 'entry-detail'),
    url(r'^/events/?$', views.EventList.as_view(), name = 'event-list'),
    url(r'^/events/(?P<pk>[0-9]+)/?$', views.EventDetail.as_view(), name = 'event-detail'),
    url(r'^/messages/?$', views.MessageList.as_view(), name = 'message-list'),
    url(r'^/messages/(?P<pk>[0-9]+)/?$', views.MessageDetail.as_view(), name = 'message-detail'),
), allowed = ['json', 'msgpack', 'csv'])