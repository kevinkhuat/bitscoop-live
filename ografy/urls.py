from __future__ import unicode_literals

from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^account', include('ografy.apps.account.urls')),
    #url(r'^api', include('ografy.apps.api.urls')),
    url(r'^blog', include('ografy.apps.blog.urls')),
    url(r'^demo', include('ografy.apps.demo.urls')),
    url(r'^docs', include('ografy.apps.documentation.urls')),
    #url(r'^extensions', include('ografy.apps.extensions.urls')),
    #url(r'^nexus', include('ografy.apps.nexus.urls')),
    #url(r'^signals', include('ografy.apps.signals.urls')),
    url(r'^user', include('ografy.apps.user.urls')),
    # Core is the primary app, and we don't want the urls prefixed with "/core".
    # So this pattern will always match and forward to "core."
    # Just be sure to put it last so it doesn't cut off the other included apps.
    url(r'^', include('ografy.apps.core.urls')),
)
