from django.conf.urls import patterns, url

import ografy.apps.obase.views as views


urlpatterns = patterns('',
    url(r'^event$', views.EventView.as_view(), name='obase_event')
)