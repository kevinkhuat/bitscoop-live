from django.conf import settings
from django.contrib.auth import _clean_credentials, login as base_login
from django.contrib.auth.signals import user_login_failed
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from ografy.util.location import get_client_ip
from ografy.apps.xauth.backends import TokenBackend, DummyTokenBackend
from ografy.apps.xauth.models import Key
from ografy.apps.xauth.util import put_address


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


def login(request, user, persist=False, track=False):
    base_login(request, user)

    if not persist:
        request.session.set_expiry(0)

    if track:
        client_ip = get_client_ip(request)
        put_address(user, client_ip)


def send_validation(strategy, backend, code):
    url = '{0}?verification_code={1}'.format(
        reverse('social:complete', args=(backend.name,)),
        code.code
    )
    url = strategy.request.build_absolute_uri(url)
    send_mail('Validate your account', 'Validate your account {0}'.format(url), settings.EMAIL_FROM, [code.email], fail_silently=False)
