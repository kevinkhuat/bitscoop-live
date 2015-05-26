import ografy.apps.core.documents as documents
import ografy.apps.core.models as models
from ografy.apps.tastydata.api import BaseApi


class AuthorizedEndpointApi(BaseApi):
    model = documents.AuthorizedEndpoint


class DataApi(BaseApi):
    model = documents.Data


class EndpointDefinitionApi(BaseApi):
    model = documents.EndpointDefinition


class EventApi(BaseApi):
    model = documents.Event


class MessageApi(BaseApi):
    model = documents.Message


class PlayApi(BaseApi):
    model = documents.Play


class ProviderApi(BaseApi):
    model = documents.Provider


class SettingsApi(BaseApi):
    model = documents.Settings


class SignalApi(BaseApi):
    model = documents.Signal


class UserApi(BaseApi):
    model = models.User
