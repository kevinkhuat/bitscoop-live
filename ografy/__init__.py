import os

from django.core.exceptions import ImproperlyConfigured


def get_path(*args):
    return os.path.abspath(os.path.join(*args))


def get_environ_setting(name, default=None):
    if name not in os.environ:
        if default is not None:
            return default

        raise ImproperlyConfigured('Environment variable {0} not set.'.format(name))

    return os.environ[name]


SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = get_path(SOURCE_PATH, '..')
