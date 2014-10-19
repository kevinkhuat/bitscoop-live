import ografy.apps.core.views as views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),
    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^contact/?$', views.contact, name='core_contact'),
)
