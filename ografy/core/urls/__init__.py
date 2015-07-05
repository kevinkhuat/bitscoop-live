from django.conf.urls import patterns, url

from ografy.core.urls import main, settings, signals

import ografy.core.views as views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),
    # TODO: Remove once the signal scheduler is integrated into the main site js
    url(r'^scheduler$', views.signal_scheduler, name='scheduler'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),

    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),
    url(r'^location_test$', views.location, name='location_test'),
) + settings.urlpatterns + signals.urlpatterns + main.urlpatterns
