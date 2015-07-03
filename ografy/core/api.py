import ografy.core.documents as documents
import ografy.core.models as models
from ografy.contrib.tastydata.api import BaseApi


class AuthorizedEndpointApi(BaseApi):
    model = documents.AuthorizedEndpoint


class DataApi(BaseApi):
    model = documents.Data

    def delete(cls, val, override=False):
        # FIXME: Make not implemented exception
        if override:
            try:
                cls.model.objects.get(pk=val).delete()
            except (TypeError, AssertionError):
                cls.model.objects.filter(val).delete()
            except cls.model.DoesNotExist:
                return False

            return True
        else:
            return False


class EndpointDefinitionApi(BaseApi):
    model = documents.EndpointDefinition


class EventApi(BaseApi):
    model = documents.Event


class MessageApi(BaseApi):
    model = documents.Message

    def delete(cls, val, override=False):
        if override:
            try:
                cls.model.objects.get(pk=val).delete()
            except (TypeError, AssertionError):
                cls.model.objects.filter(val).delete()
            except cls.model.DoesNotExist:
                return False

            return True
        else:
            return False


class PlayApi(BaseApi):
    model = documents.Play

    def delete(cls, val, override=False):
        if override:
            try:
                cls.model.objects.get(pk=val).delete()
            except (TypeError, AssertionError):
                cls.model.objects.filter(val).delete()
            except cls.model.DoesNotExist:
                return False

            return True
        else:
            return False


class ProviderApi(BaseApi):
    model = documents.Provider


class SettingsApi(BaseApi):
    model = documents.Settings


class SignalApi(BaseApi):
    model = documents.Signal


class UserApi(BaseApi):
    model = models.User
