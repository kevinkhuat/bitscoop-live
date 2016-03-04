from django.conf import settings
from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^opi', include('server.apps.opi.urls', namespace='opi')),

    url(r'', include('server.core.urls')),
)


handler400 = 'server.core.views.errors.view400'
handler403 = 'server.core.views.errors.view403'
handler404 = 'server.core.views.errors.view404'
handler500 = 'server.core.views.errors.view500'


if settings.DEBUG:
    from django.conf.urls.static import static  # isort: ignore
    from django.contrib.staticfiles.views import serve  # isort: ignore

    urlpatterns += static('/static/', view=serve)

    urlpatterns += (
        url(r'^400/?$', 'server.core.views.errors.view400'),
        url(r'^403/?$', 'server.core.views.errors.view403'),
        url(r'^404/?$', 'server.core.views.errors.view404'),
        url(r'^500/?$', 'server.core.views.errors.view500')
    )
