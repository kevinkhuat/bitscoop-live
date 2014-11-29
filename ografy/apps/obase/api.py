from ografy.util.api import BaseApi
import ografy.apps.obase.models as models
import ografy.apps.obase.documents as documents



class Signal(BaseApi):
    model = models.Signal


class Provider(BaseApi):
    model = models.Provider


class Event(BaseApi):
    model = documents.Event


class Data(BaseApi):
    model = documents.Data