import ografy.core.documents as documents
import ografy.core.models as models
from ografy.contrib.tastydata.api import BaseApi


class ContentApi(BaseApi):
    model = documents.Content


class DataApi(BaseApi):
    model = documents.Data


class EventApi(BaseApi):
    model = documents.Event


class LocationApi(BaseApi):
    model = documents.Location


class ContactApi(BaseApi):
    model = documents.Contact


class ProviderApi(BaseApi):
    model = documents.Provider


class SearchApi(BaseApi):
    model = documents.Search


class SettingsApi(BaseApi):
    model = documents.Settings


class SignalApi(BaseApi):
    model = documents.Signal


class UserApi(BaseApi):
    model = models.User
