from __future__ import unicode_literals
from django.contrib import admin
from django.conf.urls import include, patterns, url

import ografy.apps.core.errors as errors


handler400 = errors.view400
handler403 = errors.view404
handler404 = errors.view404
handler500 = errors.view500

urlpatterns = patterns('',
    url(r'^account', include('ografy.apps.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('ografy.apps.xauth.urls')),
    #url(r'^api', include('ografy.apps.api.urls')),
    url(r'^blog', include('ografy.apps.blog.urls')),
    url(r'^demo', include('ografy.apps.demo.urls')),
    url(r'^docs', include('ografy.apps.documentation.urls')),
    url(r'^obase/', include('ografy.apps.obase.urls')),
    #url(r'^extensions', include('ografy.apps.extensions.urls')),
    #url(r'^nexus', include('ografy.apps.nexus.urls')),
    #url(r'^signals', include('ografy.apps.signals.urls')),

    # All test apps to be prepended with /tests/
    url(r'^tests/auth/', include('ografy.tests.test_xauth.urls')),
    url(r'^tests/obase/', include('ografy.tests.test_obase.urls')),
    url(r'^user', include('ografy.apps.user.urls')),

    # Core is the primary app, and we don't want the urls prefixed with "/core".
    # So this pattern will always match and forward to "core."
    # Just be sure to put it last so it doesn't cut off the other included apps.
    url(r'^', include('ografy.apps.core.urls'))
)
