from django.conf.urls import patterns, url

from ografy.core.urls import main, settings, signals, user

import ografy.core.views as views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),

    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),
) + settings.urlpatterns + user.urlpatterns + signals.urlpatterns + main.urlpatterns
