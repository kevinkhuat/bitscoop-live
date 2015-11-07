from django.contrib.auth.backends import RemoteUserBackend

from server.contrib.multiauth.plugins.key.models import Key


class TokenBackend(RemoteUserBackend):
    def authenticate(self, token=None, **kwargs):
        if token is None:
            return None

        try:
            key = Key.objects.get(digest__exact=token)

            if key.is_valid:
                return key.user
        except Key.DoesNotExist:
            pass

        return None
