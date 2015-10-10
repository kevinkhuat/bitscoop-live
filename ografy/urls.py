from django.conf import settings
from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^opi', include('ografy.apps.opi.urls', namespace='opi')),
    url(r'^explore', include('ografy.apps.explorer.urls', namespace='explorer')),

    url(r'', include('ografy.core.urls')),
)


handler400 = 'ografy.core.views.errors.view400'
handler403 = 'ografy.core.views.errors.view403'
handler404 = 'ografy.core.views.errors.view404'
handler500 = 'ografy.core.views.errors.view500'


if settings.DEBUG:
    from django.conf.urls.static import static  # isort: ignore
    from django.contrib.staticfiles.views import serve  # isort: ignore

    urlpatterns += static('/static/', view=serve)

    urlpatterns += (
        url(r'^400/?$', 'ografy.core.views.errors.view400'),
        url(r'^403/?$', 'ografy.core.views.errors.view403'),
        url(r'^404/?$', 'ografy.core.views.errors.view404'),
        url(r'^500/?$', 'ografy.core.views.errors.view500')
    )
