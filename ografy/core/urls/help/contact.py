from django.conf.urls import patterns, url

import ografy.core.views.help.contact as contact_views


urlpatterns = patterns('',
    url(r'^contact/?$', contact_views.contact, name='help_contact'),
)
