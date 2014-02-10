from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from ografy.apps.core import urls as core_urls
from ografy.apps.signals import urls as signals_urls


urlpatterns = patterns('',
    url(r'^signals', include(signals_urls.urlpatterns)),
    url(r'^odata', include(core_urls.odata_v1.urls)),
    url(r'', include(core_urls.urlpatterns)),
)