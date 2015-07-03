from functools import wraps

import django.contrib.auth
import django.utils.importlib
from django.conf import settings


# This contains functions used for authenticating the current user
# Get the session engine that is in use
engine = django.utils.importlib.import_module(settings.SESSION_ENGINE)


def get_current_user(request):
    """
    This function gets the Django session cookie that was passed in by the client
    and uses it to return the user corresponding to that session.
    """
    session_key = request.get_cookie(settings.SESSION_COOKIE_NAME)

    class Dummy(object):
        pass

    django_request = Dummy()
    django_request.session = engine.SessionStore(session_key)
    user = django.contrib.auth.get_user(django_request)

    return user


def is_logged_in_user(user):
    """
    Check if user is not authenticated and not anonymous and has an ID
    """
    if hasattr(user, 'is_anonymous'):
        if user.is_anonymous():
            return False

    if hasattr(user, 'is_authenticated'):
        if not user.is_authenticated():
            return False

    if hasattr(user, 'id'):
        if user.id is not None:
            return True

    return False


def user_authenticated(fn=None):
    """
    Decorator for views that ensures that the user who made a call to the server is a valid user.
    It gets the user information from the active session ID, checks that the user is valid,
    then passes the user's information to the function that this is decorating.
    """
    @wraps(fn)
    def wrapper(self):
        current_user = get_current_user(self)

        if is_logged_in_user(current_user):
            self.request.user = current_user
            fn(self)
        else:
            return False

    return wrapper
