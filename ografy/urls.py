from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from ografy.apps.core import urls as core_urls
from ografy.apps.signals import urls as signals_urls


urlpatterns = patterns('',
    url(r'^signals/', include(signals_urls.urlpatterns)),
    url(r'^odata/', include(core_urls.odata_v1.urls)),
    # Core is the primary app, and we don't want the urls prefixed with "/core".
    # So this pattern will always match and forward to "core."
    # Just be sure to put it last so it doesn't cut off the other included apps.
    url(r'^', include(core_urls.urlpatterns)),
)
