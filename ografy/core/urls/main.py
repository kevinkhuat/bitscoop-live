from django.conf.urls import patterns, url

import ografy.core.views.main as main_views


urlpatterns = patterns('',
    # TODO: Make this general to any key we need to get, not hard-coded to Mapbox's token
    url(r'^app/keys/mapbox?$', main_views.mapbox_token, name='mapbox_token'),
)
