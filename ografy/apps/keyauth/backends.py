from django.contrib.auth.backends import RemoteUserBackend

from ografy.apps.keyauth.models import Key


class TokenBackend(RemoteUserBackend):
    def authenticate(self, token=None):
        key = Key.objects.filter(digest__exact=token).first()

        if key is not None:
            # Would probably make more sense to return the key
            # but we want to subscribe to the standard here.
            # Values are set on the User instance that need to be propagated to signals, etc.
            return key.user

        return None


class DummyTokenBackend(TokenBackend):
    def authenticate(self, *args, **kwargs):
        pass
