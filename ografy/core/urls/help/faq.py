from django.conf.urls import patterns, url

import ografy.core.views.help.faq as faq_views


urlpatterns = patterns('',
    url(r'^faq/?$', faq_views.faq, name='help_faq'),
)
