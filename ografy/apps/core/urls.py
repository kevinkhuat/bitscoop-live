from django.conf.urls import patterns, url

from tastydata.api import Api as ODataApi

from ografy.apps.core.resources import UserResource
from ografy.apps.core import views

odata_v1 = ODataApi(api_name='v1')
odata_v1.register(UserResource())

urlpatterns = patterns('',
    url(r'^/?$', views.index)
)
