from django.db.models import Q as D_Q
from mongoengine import Q as M_Q

import ografy.apps.core.documents as documents
import ografy.apps.core.models as models
from ografy.apps.tastydata.api import BaseApi
from ografy.apps.tastydata.parse import ViewApi


class ProviderApi(BaseApi):
    Q = D_Q
    model = models.Provider


# TODO: Merge free fields on User object with MongoDB data on GET. Save appropriately (route the properties) on a PATCH.
class SettingsApi(BaseApi):
    Q = M_Q
    model = documents.Settings


class SignalApi(BaseApi):
    Q = D_Q
    model = models.Signal


class UserApi(BaseApi):
    Q = D_Q
    model = models.User

# TODO: Move to Serializer, Tastadata View, or View?
class ProviderViewApi(ProviderApi, ViewApi):
    is_mongo_query = False


class SettingsViewApi(SettingsApi, ViewApi):
    is_mongo_query = True


class SignalViewApi(SignalApi, ViewApi):
    is_mongo_query = False


class UserViewApi(UserApi, ViewApi):
    is_mongo_query = False
