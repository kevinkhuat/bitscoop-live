import inspect

from django.conf import settings
from django.contrib.auth import _clean_credentials, _get_user_session_key, BACKEND_SESSION_KEY, HASH_SESSION_KEY, load_backend, login as base_login, logout as base_logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_login_failed
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.crypto import constant_time_compare


__all__ = ('authenticate', 'login', 'logout',)


def authenticate(backends=settings.AUTHENTICATION_BACKENDS, exclude={}, **credentials):
    resolved_backends = [load_backend(backend_path) for backend_path in backends if backend_path not in exclude]

    if not resolved_backends:
        raise ImproperlyConfigured('No authentication backends have been defined. Does AUTHENTICATION_BACKENDS contain anything?')

    for backend in resolved_backends:
        try:
            inspect.getcallargs(backend.authenticate, **credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue

        try:
            user = backend.authenticate(**credentials)
        except PermissionDenied:
            # This backend says to stop in our tracks - this user should not be allowed in at all.
            return None

        if user is None:
            continue

        # Annotate the user object with the path of the backend.
        user.backend = '%s.%s' % (backend.__module__, backend.__class__.__name__)

        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials))


def get_user(request):
    user = None

    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)

        if 'django.contrib.auth.middleware.SessionAuthenticationMiddleware' in settings.MIDDLEWARE_CLASSES and hasattr(user, 'get_session_auth_hash'):
            session_hash = request.session.get(HASH_SESSION_KEY)
            session_hash_verified = session_hash and constant_time_compare(session_hash, user.get_session_auth_hash())
            if not session_hash_verified:
                request.session.flush()
                user = None

    return user or AnonymousUser()


def login(request, user, persist=False):
    base_login(request, user)

    if not persist:
        request.session.set_expiry(0)


def logout(request):
    # We need to put these plugin logout methods first because the base logout method flushes the session and sets the
    # request user to the AnonymousUser. This would hinder any attempts to access user or session data during the logout
    # process.
    backend_name = request.session.get(BACKEND_SESSION_KEY)

    if backend_name:
        try:
            backend = load_backend(backend_name)

            if hasattr(backend, 'deauthenticate'):
                backend.deauthenticate(request)
        except ImportError:
            return

    base_logout(request)
