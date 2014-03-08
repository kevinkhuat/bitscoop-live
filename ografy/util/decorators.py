from functools import wraps

from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils.decorators import available_attrs


def autoconnect(cls):
    """
    Class decorator that automatically connects pre_save / post_save signals on
    a model class to its pre_save() / post_save() methods.
    """
    def connect(signal, func):
        cls.func = staticmethod(func)

        @wraps(func)
        def wrapper(sender, **kwargs):
            return func(kwargs.get('instance'))

        signal.connect(wrapper, sender=cls)

        return wrapper

    if hasattr(cls, 'pre_save'):
        cls.pre_save = connect(pre_save, cls.pre_save)

    if hasattr(cls, 'post_save'):
        cls.post_save = connect(post_save, cls.post_save)

    return cls


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
    decorator = user_passes_test(lambda u: u.is_authenticated())

    if function:
        return decorator(function)

    return decorator
