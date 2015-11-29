import server.core.documents as documents
import server.core.models as models
from server.contrib.tastydata.api import BaseApi


class ProviderApi(BaseApi):
    model = documents.Provider


class SettingsApi(BaseApi):
    model = documents.Settings


class ConnectionApi(BaseApi):
    model = documents.Connection


class UserApi(BaseApi):
    model = models.User
