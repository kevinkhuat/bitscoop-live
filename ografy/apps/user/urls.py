from django.conf.urls import patterns, url

from ografy.apps.user import views


urlpatterns = patterns('',
    url(r'^/(?P<handle>\w+)/?$', views.profile, name='user_profile'),
    url(r'^/?$', views.my_profile, name='user_my_profile'),
)
