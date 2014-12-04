from django.conf.urls import patterns, url

import ografy.apps.obase.views as views

urlpatterns = patterns('',
    url(r'^data/?$', views.DataGroupView.as_view(), name='obase_group_data'),
    url(r'^data/(?P<val>[^/]+)/?$', views.DataSingleView.as_view(), name='obase_single_data'),
    url(r'^event/$', views.EventGroupView.as_view(), name='obase_group_event'),
    url(r'^event/(?P<val>[^/]+)/?$', views.EventSingleView.as_view(), name='obase_single_event'),
    url(r'^message/?$', views.MessageGroupView.as_view(), name='obase_group_message'),
    url(r'^message/(?P<val>[^/]+)/?$', views.MessageSingleView.as_view(), name='obase_single_message'),
    url(r'^provider/?$', views.ProviderGroupView.as_view(), name='obase_group_provider'),
    url(r'^provider/(?P<val>[^/]+)/?$', views.ProviderSingleView.as_view(), name='obase_single_provider'),
    url(r'^signal/?$', views.SignalGroupView.as_view(), name='obase_group_signal'),
    url(r'^signal/(?P<val>[^/]+)/?$', views.ProviderSingleView.as_view(), name='obase_single_signal')
)
