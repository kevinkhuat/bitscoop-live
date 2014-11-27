import ografy.apps.xauth.models as models
from ografy.util.api import BaseApi


class Address(BaseApi):
    model = models.Address


class Key(BaseApi):
    model = models.Key


class User(BaseApi):
    model = models.User
