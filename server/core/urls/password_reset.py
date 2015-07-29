from django.conf.urls import patterns, url

import server.core.views.password_reset as views


urlpatterns = patterns('',
    url(r'^recover/?$', views.Recover.as_view(), name='recover'),
    url(r'^recover/sent/?$', views.RecoverSent.as_view(), name='recover-sent'),
    url(r'^reset/done/?$', views.ResetDone.as_view(), name='reset-done'),
    url(r'^reset/(?P<token>[a-f0-9]+)/?$', views.Reset.as_view(), name='reset'),
)
