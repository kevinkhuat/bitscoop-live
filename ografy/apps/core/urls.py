from django.conf.urls import patterns, url

from ografy.apps.core import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),
)
