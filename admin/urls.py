from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
)
