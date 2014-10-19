from django.conf.urls import patterns, url

import ografy.apps.auth.views as views


urlpatterns = patterns('',
    # Ografy Account specific login/logout
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),

    # Python Social Auth Specific Workflow
    url(r'^associate/(?P<backend>[^/]+)/$', views.associate, name='auth_associate'),
    url(r'^call/(?P<backend>[^/]+)/$', views.call, name='auth_call'),
    url(r'^signals/$', views.signals, name='auth_signals'),
    url(r'^proxy/$', views.proxy, name='auth_proxy'),
    url(r'^signature/(?P<backend>[^/]+)/$', views.signature, name='auth_signature')
)
