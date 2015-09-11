from functools import wraps

from django.conf import settings
from django.utils.decorators import available_attrs
from django.utils.module_loading import import_string


_MULTIAUTH_AUTH_ERROR = getattr(settings, 'MULTIAUTH_AUTH_ERROR', 'django.core.exceptions.PermissionDenied')
_AUTH_ERROR_CLASS = import_string(_MULTIAUTH_AUTH_ERROR)


def user_passes_test(test_fn, exception=_AUTH_ERROR_CLASS):
    if isinstance(exception, str):
        exception = import_string(exception)

    def decorator(view_fn):
        @wraps(view_fn, assigned=available_attrs(view_fn))
        def _wrapped_view(request, *args, **kwargs):
            if test_fn(request.user):
                return view_fn(request, *args, **kwargs)

            raise exception

        return _wrapped_view

    return decorator


def login_required(function=None, exception=_AUTH_ERROR_CLASS):
    """
    Decorator for views that checks that the user is logged in.
    If not a PermissionDenied exception is raised.
    """
    actual_decorator = user_passes_test(lambda u: u.is_authenticated(), exception=exception)

    if function:
        return actual_decorator(function)

    return actual_decorator


def permission_required(perm, exception=_AUTH_ERROR_CLASS):
    """
    Decorator for views that checks whether a user has a particular permission enabled.
    If not a PermissionDenied exception is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anonymous users)
        if user.has_perm(perm):
            return True

    return user_passes_test(check_perms, exception=exception)


def membership_required(group, exception=_AUTH_ERROR_CLASS):
    """
    Decorator for views that checks whether a user is a member of a particular group.
    If the logged in user is not a member of the specified group a PermissionDenied exception is raised.
    """
    def check_group(user):
        if not user.is_anonymous() and user.member_of(group):
            return True

    return user_passes_test(check_group, exception=exception)
