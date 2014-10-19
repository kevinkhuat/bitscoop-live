from __future__ import unicode_literals
from functools import wraps

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs

from ografy.apps.auth import authenticate, login
from ografy.apps.auth.models import Key


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


def user_passes_test(test_fn, exception=PermissionDenied):
    def decorator(view_fn):
        @wraps(view_fn, assigned=available_attrs(view_fn))
        def _wrapped_view(request, *args, **kwargs):
            if test_fn(request.user):
                return view_fn(request, *args, **kwargs)

            raise exception

        return _wrapped_view

    return decorator


def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(lambda u: u.is_authenticated())

    if function:
        return actual_decorator(function)

    return actual_decorator


def permission_required(perm):
    """
    Decorator for views that checks whether a user has a particular permission enabled.
    If not a PermissionDenied exception is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True

    return user_passes_test(check_perms)


def membership_required(group):
    """
    Decorator for views that checks whether a user is a member of a particular group.
    If the logged in user is not a member of the specified group a PermissionDenied exception is raised.
    """
    def check_group(user):
        # FIXME: This is a junky hack for anonymous users.
        if not isinstance(user, AnonymousUser) and user.member_of(group):
            return True

    return user_passes_test(check_group)
