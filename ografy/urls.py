from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from ografy.apps.core import urls as core_urls

urlpatterns = patterns('',
    url(r'^odata', include(core_urls.odata_v1.urls)),
    url(r'', include(core_urls.urlpatterns)),
)