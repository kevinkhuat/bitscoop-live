from __future__ import unicode_literals

import six
from django.conf import settings
from tastypie.exceptions import BadRequest
from tastypie.paginator import Paginator as BasePaginator

from ografy.lib.tastydata.util import get_query_string


class Paginator(BasePaginator):
    def get_limit(self):
        """
        Determines the proper maximum number of results to return.

        In order of importance, it will use:
            * The user-requested ``limit`` from the GET parameters, if specified.
            * The object-level ``limit`` if specified.
            * ``settings.API_LIMIT_PER_PAGE`` if specified.
        """

        max_limit = getattr(settings, 'TASTYDATA_PAGE_LIMIT', 20)
        limit = self.request_data.get('$top', max_limit)

        try:
            limit = int(limit)
        except ValueError:
            raise BadRequest('Invalid limit `%s` provided. Please provide a positive integer.' % limit)

        if limit < 0:
            raise BadRequest('Invalid limit `%s` provided. Please provide a positive integer >= 0.' % limit)

        return limit if limit < max_limit else max_limit

    def get_offset(self):
        """
        Determines the proper starting offset of results to return.

        It attempts to use the user-provided ``offset`` from the GET parameters,
        if specified.
        """
        offset = self.request_data.get('$skip', 0)

        try:
            offset = int(offset)
        except ValueError:
            raise BadRequest('Invalid offset `%s` provided. Please provide an integer.' % offset)

        if offset < 0:
            raise BadRequest('Invalid offset `%s` provided. Please provide a positive integer >= 0.' % offset)

        return offset

    def _generate_uri(self, limit, offset):
        if self.resource_uri is None:
            return None

        try:
            request_params = self.request_data.copy()
        except AttributeError:
            request_params = {}

            for key, value in self.request_data.items():
                if isinstance(value, six.text_type):
                    request_params[key] = value.encode('utf-8')
                else:
                    request_params[key] = value

        request_params.update({
            '$top': limit,
            '$skip': offset
        })
        encoded_params = get_query_string(request_params)

        return '%s?%s' % (self.resource_uri, encoded_params)

    def page(self):
        """
        Generates all pertinent data about the requested page.

        Handles getting the correct ``limit`` & ``offset``, then slices off
        the correct set of results and returns all pertinent metadata.
        """
        limit = self.get_limit()
        offset = self.get_offset()
        count = self.get_count()
        objects = self.get_slice(limit, offset)
        meta = {
            'offset': offset,
            'limit': limit,
            'count': count,
        }

        if limit:
            meta['previous'] = self.get_previous(limit, offset)
            meta['next'] = self.get_next(limit, offset, count)

        return {
            'objects': objects,
            'meta': meta,
        }
