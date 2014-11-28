from django.conf.urls import patterns, url

import ografy.apps.obase.views as views
from ografy.apps.obase.documents import Event


urlpatterns = patterns('',
    url(r'^event$', views.EventGroupView.as_view(), name='obase_group_event'),
    url(r'^event/(?P<id>[^/]+)$', views.EventSingleView.as_view(), name='obase_single_event'),
    url(r'^test', views.EventGroupView.get, name='obase_test'),
)
