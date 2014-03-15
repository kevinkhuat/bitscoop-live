from __future__ import unicode_literals

from django.contrib.auth import _clean_credentials, login as base_login
from django.contrib.auth.signals import user_login_failed
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now

from ografy.apps.keyauth.backends import TokenBackend, DummyTokenBackend
from ografy.apps.keyauth.models import Key


def authenticate(**credentials):
    try:
        user = TokenBackend().authenticate(**credentials)
    except PermissionDenied:
        pass

    if user is not None:
        # We want to record DummyTokenBackend as the recorded backend so that we can remove TokenBackend from the
        # settings list. The goal is to call TokenBackend explicitly so that typical users cannot authenticate with a
        # token on the login page. We want to be able to authenticate on a request-by-request basis.
        user.backend = '{0}.{1}'.format(DummyTokenBackend.__module__, DummyTokenBackend.__name__)

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
