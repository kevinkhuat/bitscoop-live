from django.conf import settings
from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^opi', include('ografy.apps.opi.urls')),


    url(r'^', include('ografy.core.urls')),
)


handler400 = 'ografy.core.views.errors.view400'
handler403 = 'ografy.core.views.errors.view403'
handler404 = 'ografy.core.views.errors.view404'
handler500 = 'ografy.core.views.errors.view500'


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # isort: ignore
    urlpatterns += staticfiles_urlpatterns()
