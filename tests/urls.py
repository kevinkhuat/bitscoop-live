from django.conf.urls import include, patterns, url

import ografy.errors as errors


handler400 = errors.view400
handler403 = errors.view404
handler404 = errors.view404
handler500 = errors.view500

urlpatterns = patterns('',
    url(r'^auth', include('ografy.apps.xauth.urls')),
    #url(r'^help', include('ografy.apps.helpr.urls')),
    url(r'^opi', include('ografy.apps.opi.urls')),

    # Core is the primary app, and we don't want the urls prefixed with "/core".
    # So this pattern will always match and forward to "core."
    # Just be sure to put it last so it doesn't cut off the other included apps.
    url(r'^', include('ografy.apps.core.urls')),

    url(r'^tests/auth', include('ografy.tests.xauth.urls')),
    # url(r'^tests/obase', include('ografy.tests.test_obase.urls')),
)
