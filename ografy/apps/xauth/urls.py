from django.conf.urls import patterns, url, include

import ografy.apps.xauth.views as views


urlpatterns = patterns('',
    # Ografy Account specific login/logout
    url(r'^applogin/?$', views.LoginView.as_view(), name='xauth_login'),
    url(r'^applogout/?$', views.logout, name='xauth_logout'),

    # Python Social Auth Specific Workflow
    url(r'^associate/(?P<backend>[^/]+)/$', views.associate, name='xauth_associate'),
    url(r'^call/(?P<backend>[^/]+)/$', views.call, name='xauth_call'),
    url(r'^signals/?$', views.signals, name='xauth_signals'),
    url(r'^proxy/?$', views.proxy, name='xauth_proxy'),
    url(r'^signature/(?P<backend>[^/]+)/$', views.signature, name='xauth_signature'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)
