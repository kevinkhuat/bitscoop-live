import ografy.core.documents as documents
import ografy.core.models as models
from ografy.contrib.tastydata.api import BaseApi


class ProviderApi(BaseApi):
    model = documents.Provider


class SettingsApi(BaseApi):
    model = documents.Settings


class SignalApi(BaseApi):
    model = documents.Signal


class UserApi(BaseApi):
    model = models.User
