from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^/', include('social.apps.django_app.urls', namespace='social'))
)
