from __future__ import unicode_literals
from django.conf.urls import include, patterns, url
from ografy.apps.core import urls as core_urls
from ografy.apps.core.api import SimpleBlobResource
from django.contrib import admin

admin.autodiscover()
api_resource = SimpleBlobResource()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^odata', include(core_urls.odata_v1.urls)),
    url(r'', include(core_urls.urlpatterns)),
    (r'^api/', include(api_resource.urls)),
)