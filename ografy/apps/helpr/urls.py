from django.conf.urls import patterns, url

from ografy.apps.helpr import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='helpr_index'),
)
