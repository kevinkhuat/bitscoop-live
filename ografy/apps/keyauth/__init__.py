from __future__ import unicode_literals

from django.contrib.auth import _clean_credentials, login as base_login
from django.contrib.auth.signals import user_login_failed
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now

from ografy.apps.keyauth.backends import TokenBackend
from ografy.apps.keyauth.models import Key


def authenticate(**credentials):
    try:
        user = TokenBackend().authenticate(**credentials)
    except PermissionDenied:
        pass

    if user is not None:
        user.backend = '{0}.{1}'.format(TokenBackend.__module__, TokenBackend.__name__)

        return user

    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials))


def login(request, user, key, persist=False, track=False):
    base_login(request, user)

    key.last_login = now()
    key.login_count += 1
    key.save()

    if not persist:
        request.session.set_expiry(0)

    if track:
        client_ip = request.META['REMOTE_ADDR']
        key.put_address(client_ip)
