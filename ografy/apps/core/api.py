from django.db.models import Q as Django_Q
from mongoengine import Q as Mongo_Q

import ografy.apps.core.documents as documents
import ografy.apps.core.models as models
from ografy.apps.tastydata.api import BaseApi
from ografy.apps.tastydata.parse import ViewApi


class ProviderApi(BaseApi):
    Q = Django_Q
    model = models.Provider


# TODO: Merge free fields on User object with MongoDB data on GET. Save appropriately (route the properties) on a PATCH.
class SettingsApi(BaseApi):
    Q = Mongo_Q
    model = documents.Settings


class SignalApi(BaseApi):
    Q = Django_Q
    model = models.Signal


class UserApi(BaseApi):
    Q = Django_Q
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
