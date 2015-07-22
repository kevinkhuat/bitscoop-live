from django.conf.urls import include, patterns, url

from ografy.core.urls import main, settings, signals
from ografy.core.urls.help import contact, documentation

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

    url(r'^settings/', include(settings.urlpatterns)),
    url(r'', include(signals.urlpatterns)),
    url(r'^app/', include(main.urlpatterns)),
    url(r'^help/documentation/', include(documentation.urlpatterns)),
    url(r'^help/', include(contact.urlpatterns)),
)
