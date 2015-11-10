from functools import wraps

from django.utils.decorators import available_attrs

from server.contrib.pytoolbox.django import get_content_type


def accepted_types(types={'text/html'}, default_type='text/html'):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            request.response_type = get_content_type(request.accepted_types, types, default_type)

            return func(request, *args, **kwargs)

        return inner

    return decorator
