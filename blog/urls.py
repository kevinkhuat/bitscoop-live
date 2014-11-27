from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^blog', include('ografy.apps.blog.urls'))
)
