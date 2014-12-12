from django.conf.urls import patterns, url

import ografy.apps.core.views as views
import ografy.apps.core.views.settings as settings_views
import ografy.apps.core.views.user as user_views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),

    url(r'^settings/?$', settings_views.base, name='core_settings_personal'),
    url(r'^settings/personal/?$', settings_views.PersonalView.as_view(), name='core_settings_personal'),
    url(r'^settings/security/?$', settings_views.SecurityView.as_view(), name='core_settings_security'),
    url(r'^settings/signals/?$', settings_views.SignalView.as_view(), name='core_settings_signals'),

    url(r'^user/?$', user_views.my_profile, name='core_user_my_profile'),
    url(r'^user/(?P<handle>\w+)/?$', user_views.profile, name='core_user_profile'),
    url(r'^providers/?$', user_views.providers, name='core_providers'),
    url(r'^signals/?$', settings_views.SignalView.as_view(), name='core_signals'),
    url(r'^signals/(?P<pk>[a-zA-Z0-9]+)/?$', user_views.signals, name='core_signals'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),
    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),
)
