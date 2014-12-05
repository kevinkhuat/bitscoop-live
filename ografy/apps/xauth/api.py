import ografy.apps.xauth.models as models
from ografy.apps.tastydata.api import BaseApi


class Address(BaseApi):
    model = models.Address


class Key(BaseApi):
    model = models.Key
