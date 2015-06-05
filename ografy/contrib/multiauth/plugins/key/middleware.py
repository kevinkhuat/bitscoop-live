from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.core.cache import caches
from django.utils import timezone

from ografy.contrib.multiauth.plugins.key import CACHE_PREFIX
from ografy.contrib.multiauth.plugins.key.models import Key


if hasattr(settings, 'MULTIAUTH_CACHE'):
    cache = caches[settings.MULTIAUTH_CACHE]
else:
    cache = None


# FIXME: Make this middleware.
class TokenBackend(RemoteUserBackend):
    @staticmethod
    def _get_cache_key(token):
        return '{0}:{1}'.format(CACHE_PREFIX, token)

    def authenticate(self, token=None, **kwargs):
        if token is None:
            return None

        user = None

        if cache:
            cache_key = TokenBackend._get_cache_key(token)
            user_id = cache.get(cache_key)

            if user_id:
                UserModel = get_user_model()

                try:
                    user = UserModel.objects.get(pk=user_id)
                except UserModel.DoesNotExist:
                    pass

        if not user:
            try:
                key = Key.objects.get(digest__exact=token)

                if key.is_valid:
                    user = key.user
            except Key.DoesNotExist:
                pass

        if cache and hasattr(user, 'is_anonymous') and not user.is_anonymous():
            # FIXME: Calculate expiration for cache TTL?
            if key.expires:
                ttl = (key.expires - timezone.now()).seconds
                cache.set(cache_key, key.user.pk, TIMEOUT=ttl)
            else:
                cache.set(cache_key, key.user.pk)

        return user
