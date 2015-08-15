from django.conf.urls import include, patterns, url

from ografy.core.urls import main, settings, signals
from ografy.core.urls.help import contact, documentation, faq

import ografy.core.views as views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),

    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),

    url(r'^settings/', include(settings.urlpatterns)),
    url(r'', include(signals.urlpatterns)),
    url(r'^app/', include(main.urlpatterns)),
    url(r'^help/documentation/', include(documentation.urlpatterns)),
    url(r'^help/', include(contact.urlpatterns)),
    url(r'^help/', include(faq.urlpatterns)),
)
