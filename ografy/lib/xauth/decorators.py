from __future__ import unicode_literals
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs

from ografy.lib.xauth import authenticate, login
from ografy.lib.xauth.models import Key


def token_required(view_fn, exception=PermissionDenied):
    """
    Decorator that ensures the user has provided a valid token.
    """
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        token = request.REQUEST.get('token')
        # TODO: Can this be memcached? Probably... take a look into Django cache middleware.
        key = Key.objects.filter(digest__exact=token).first()

        if key is None or not key.is_valid:
            raise exception

        request.key = key

        return view_fn(request, *args, **kwargs)

    return _wrapped_view


def key_login(view_fn, persist=False, track=True, exception=PermissionDenied):
    """
    Decorator to manage a key login view.
    """
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        token = request.REQUEST.get('token')

        user = authenticate(token=token)
        if user is None or not user.is_valid:
            raise exception

        login(request, user, persist=persist, track=track)

        return view_fn(request, *args, **kwargs)

    return _wrapped_view
