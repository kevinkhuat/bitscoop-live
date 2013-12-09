from django.conf.urls import patterns, url

from tastydata.api import Api as ODataApi

from ografy.apps.core.resources import AccountResource, EntryResource, UserResource
from ografy.apps.core import views

odata_v1 = ODataApi(api_name='v1')
odata_v1.register(UserResource())
odata_v1.register(AccountResource())
odata_v1.register(EntryResource())

urlpatterns = patterns('',
    url(r'^/?$', views.index)
)
