from __future__ import unicode_literals

from django.utils.text import slugify as base_slugify
import six


def slugify(value):
    unic = six.u(value)

    return base_slugify(unic)
