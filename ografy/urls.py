from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^account', include('ografy.apps.account.urls')),
    url(r'^blog', include('ografy.apps.blog.urls')),
    url(r'^demo', include('ografy.apps.demo.urls')),
    url(r'^help', include('ografy.apps.helpr.urls')),
    url(r'^user', include('ografy.apps.user.urls')),
    url(r'^auth/', include('ografy.apps.xauth.urls')),

    # All test apps to be prepended with /tests/
    url(r'^tests/auth', include('ografy.tests.xauth.urls')),

    # Core is the primary app, and we don't want the urls prefixed with "/core".
    # So this pattern will always match and forward to "core."
    # Just be sure to put it last so it doesn't cut off the other included apps.
    url(r'^', include('ografy.apps.core.urls'))
)
