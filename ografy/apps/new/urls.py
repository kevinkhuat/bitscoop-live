from django.conf.urls import patterns, url


urlpatterns = patterns('ografy.apps.new.views',
    url(r'^/?$', 'index', name='new_index'),
)
