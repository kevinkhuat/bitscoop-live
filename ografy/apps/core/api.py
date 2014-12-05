import ografy.apps.core.documents as documents
import ografy.apps.core.models as models
from ografy.apps.tastydata.api import BaseApi


class ProviderApi(BaseApi):
    model = models.Provider


class SettingsApi(BaseApi):
    model = documents.Settings

    # TODO: Merge free fields on User object with MongoDB data on GET. Save appropriately (route the properties) on a PATCH.


class SignalApi(BaseApi):
    model = models.Signal


class UserApi(BaseApi):
    model = models.User
