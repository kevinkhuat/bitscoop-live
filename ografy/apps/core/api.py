import ografy.apps.core.documents as documents
import ografy.apps.core.models as models
from ografy.apps.tastydata.api import BaseApi


class ProviderApi(BaseApi):
    model = models.Provider

class SettingsApi(BaseApi):
    model = documents.Settings

class SignalApi(BaseApi):
    model = models.Signal

class UserApi(BaseApi):
    model = models.User
