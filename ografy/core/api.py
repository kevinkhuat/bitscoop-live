import ografy.core.documents as documents
import ografy.core.models as models
from ografy.contrib.tastydata.api import BaseApi


class PermissionApi(BaseApi):
    model = documents.Permission


class DataApi(BaseApi):
    model = documents.Data

    @classmethod
    def delete(cls, val):
        raise NotImplementedError(
            'Cannot delete documents that reference Event; '
            'delete the associated Event in order to delete reference documents'
        )


class EndpointApi(BaseApi):
    model = documents.Endpoint


class EventApi(BaseApi):
    model = documents.Event


class LocationApi(BaseApi):
    model = documents.Location


class MessageApi(BaseApi):
    model = documents.Message

    @classmethod
    def delete(cls, val):
        raise NotImplementedError(
            'Cannot delete documents that reference Event; '
            'delete the associated Event in order to delete reference documents'
        )


class PlayApi(BaseApi):
    model = documents.Play

    @classmethod
    def delete(cls, val):
        raise NotImplementedError(
            'Cannot delete documents that reference Event; '
            'delete the associated Event in order to delete reference documents'
        )


class ProviderApi(BaseApi):
    model = documents.Provider


class SettingsApi(BaseApi):
    model = documents.Settings


class SignalApi(BaseApi):
    model = documents.Signal


class UserApi(BaseApi):
    model = models.User
