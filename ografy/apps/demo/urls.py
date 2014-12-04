from django.conf.urls import patterns, url

from ografy.apps.demo import views


urlpatterns = patterns('',
    url(r'^$', views.login, name='demo_login'),

    url(r'^info/?$', views.info, name='demo_info'),
    url(r'^examples/?$', views.examples, name='demo_examples'),
    url(r'^resources/?$', views.resources, name='demo_resources'),

    # url(r'^/dashboard/?$', views.dashboard, name='demo_dashboard'),
    # url(r'^/infographic/?$', views.infographic, name='demo_infographic'),

    url(r'^map/?$', views.map, name='demo_map'),
    url(r'^timeline/?$', views.timeline, name='demo_timeline'),
)
