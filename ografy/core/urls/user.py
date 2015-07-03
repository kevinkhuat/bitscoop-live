from django.conf.urls import patterns, url

import ografy.core.views.user as user_views


urlpatterns = patterns('',
    url(r'^user/?$', user_views.my_profile, name='core_user_my_profile'),
    url(r'^user/(?P<handle>\w+)/?$', user_views.profile, name='core_user_profile'),
    url(r'^signals/(?P<pk>[a-zA-Z0-9]+)/?$', user_views.signals, name='core_signals'),
)
