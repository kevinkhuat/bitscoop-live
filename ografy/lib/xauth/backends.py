from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, RemoteUserBackend

from ografy.lib.xauth.models import Key


class IdentifierBackend(ModelBackend):
    def authenticate(self, identifier=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = UserModel.objects.by_identifier(identifier).first()

        if user is not None and user.check_password(password):
            return user


class TokenBackend(RemoteUserBackend):
    def authenticate(self, token=None, **kwargs):
        key = Key.objects.filter(digest__exact=token).first()

        if key is not None and key.is_valid:
            # Would probably make more sense to return the key
            # but we want to subscribe to the standard here.
            # Values are set on the User instance that need to be propagated to signals, etc.
            return key.user

        return None


class DummyTokenBackend(TokenBackend):
    def authenticate(self, *args, **kwargs):
        pass
