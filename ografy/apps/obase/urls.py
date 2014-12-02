from django.conf.urls import patterns, url

import ografy.apps.obase.views as views
import ografy.apps.obase.tests as test

urlpatterns = patterns('',
    url(r'^data$', views.DataGroupView.as_view(), name='obase_group_data'),
    url(r'^data/(?P<id>[^/]+)$', views.DataSingleView.as_view(), name='obase_single_data'),
    url(r'^event$', views.EventGroupView.as_view(), name='obase_group_event'),
    url(r'^event/(?P<id>[^/]+)$', views.EventSingleView.as_view(), name='obase_single_event'),
    url(r'^message$', views.MessageGroupView.as_view(), name='obase_group_message'),
    url(r'^message/(?P<id>[^/]+)$', views.MessageSingleView.as_view(), name='obase_single_message'),
    url(r'^provider', views.ProviderGroupView.as_view(), name='obase_group_provider'),
    url(r'^provider/(?P<id>[^/]+)$', views.ProviderSingleView.as_view(), name='obase_single_provider'),
    url(r'^signal', views.SignalGroupView.as_view(), name='obase_group_signal'),
    url(r'^signal/(?P<id>[^/]+)$', views.ProviderSingleView.as_view(), name='obase_single_signal'),
    url(r'^test', test.TestoBase.test_Message, name='obase_data_test')
)
