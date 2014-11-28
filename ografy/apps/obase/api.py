import ografy.apps.obase.models as models
from ografy.util.api import BaseApi


class Signal(BaseApi):
    model = models.Signal


class Provider(BaseApi):
    model = models.Provider
