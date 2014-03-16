from __future__ import unicode_literals

from tastydata.api import Api as ODataApi

from ografy.apps.api.resources import AccountResource, EntryResource, UserResource


odata_v1 = ODataApi(api_name='v1')
odata_v1.register(UserResource())
odata_v1.register(AccountResource())
odata_v1.register(EntryResource())

urlpatterns = odata_v1.urls
