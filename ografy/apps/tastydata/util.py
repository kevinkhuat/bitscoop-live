from __future__ import unicode_literals

import six

import mimeparse
from tastypie.exceptions import BadRequest, InvalidFilterError

try:
    import urllib.parse as urlparse
except ImportError:
    import urllib as urlparse


CONTROL_PARAMS = {'$filter', '$set', '$skip', '$top'}


def get_query_string(kwargs={}):
    params = []

    for key, value in six.iteritems(kwargs):
        formatted_key = key if key in CONTROL_PARAMS else urlparse.quote(key)
        formatted_value = urlparse.quote(str(value))
        params.append('%s=%s' % (formatted_key, formatted_value))

    return '&'.join(params)


def get_literal_value(value):
    if value == 'True' or value == 'true':
        return True
    elif value == 'False' or value == 'false':
        return False
    elif value[0] == '\'' and value[-1] == '\'':
        return value[1:-1]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    raise InvalidFilterError('Invalid literal: `{0}`'.format(value))


def get_mime_format(request, serializer, default_format='application/json'):
    """
    Tries to "smartly" determine which output format is desired.

    First attempts to find a ``format`` override from the request and supplies
    that if found.

    If no request format was demanded, it falls back to ``mimeparse`` and the
    ``Accepts`` header, allowing specification that way.

    If still no format is found, returns the ``default_format`` (which defaults
    to ``application/json`` if not provided).

    NOTE: callers *must* be prepared to handle BadRequest exceptions due to
          malformed HTTP request headers!
    """
    # First, check if they forced the format.
    if request.GET.get('$format'):
        if request.GET['$format'] in serializer.formats:
            return serializer.get_mime_for_format(request.GET['$format'])

    # Try to fallback on the Accepts header.
    if request.META.get('HTTP_ACCEPT', '*/*') != '*/*':
        formats = list(serializer.supported_formats) or []
        # Reverse the list, because mimeparse is weird like that. See also
        # https://github.com/toastdriven/django-tastypie/issues#issue/12 for
        # more information.
        formats.reverse()

        try:
            best_format = mimeparse.best_match(formats, request.META['HTTP_ACCEPT'])
        except ValueError:
            raise BadRequest('Invalid Accept header')

        if best_format:
            return best_format

    # No valid 'Accept' header/formats. Sane default.
    return default_format