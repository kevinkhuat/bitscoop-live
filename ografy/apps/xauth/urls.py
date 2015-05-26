from django.conf.urls import include, patterns, url


urlpatterns = patterns('',  # noqa
    url(r'^/', include('social.apps.django_app.urls', namespace='social'))
)
