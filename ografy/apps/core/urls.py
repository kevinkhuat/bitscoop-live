from django.conf.urls import patterns, url

from ografy.apps.core import views


urlpatterns = patterns('',
    url(r'^/?$', views.index),
    url(r'^dashboard/?$', views.dashboard),
    url(r'^login/?$', views.LoginView.as_view()),
)
