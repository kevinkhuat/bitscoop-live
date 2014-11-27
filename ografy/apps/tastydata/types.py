import mimeparse

from ografy.apps.tastydata.exceptions import BadRequest


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
