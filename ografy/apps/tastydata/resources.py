from __future__ import unicode_literals
import json

from django.conf.urls import patterns, url
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.constants import QUERY_TERMS
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError
from tastypie.resources import ModelResource as BaseResource

from ografy.apps.tastydata.filters import parse_filter
from ografy.apps.tastydata.paginator import Paginator
from ografy.apps.tastydata.serializers import Serializer
from ografy.apps.tastydata.util import get_mime_format


class Resource(BaseResource):
    def __init__(self, *args, **kwargs):
        # Initialize the Resource as a BaseResource
        super(Resource, self).__init__(*args, **kwargs)

        # If the Resource specification does not have a `serializer` property
        # then it will use the default django-tastypie serializer.
        # Since we've implemented a django-tastydata serializer we want to use it as the default
        # without mucking about in the django-tastypie source. So just overwrite the RESULT
        # of the relevant initialization.
        # FIXME: This is a bit hacky. Is there a better solution?
        # TODO: Look into a more future-proof fix for this.
        # TODO: Do we want more modular serialization like django-rest-framework? Probably...
        if not hasattr(self, 'Meta') or not hasattr(self.Meta, 'paginator_class'):
            self._meta.paginator_class = Paginator

        if not hasattr(self, 'Meta') or not hasattr(self.Meta, 'serializer'):
            self._meta.serializer = Serializer()

    @property
    def primary_key_name(self):
        """
        The name of the primary key field of this `Resource` instance's underlying Django model.
        """
        # Accessing a private member on the root object class so we can get at
        # the PK name from the actual django model rather than the tastypie resource.
        return self._meta.object_class._meta.pk.name

    @property
    def odata_resource_name(self):
        """
        The OData collection name for this `Resource`.
        """
        return self._meta.resource_name.capitalize()

    @property
    def urls(self):
        """
        The OData URLs this `Resource` instance should respond to.
        """

        resource_name = self.odata_resource_name
        detail_name = self._meta.detail_uri_name

        list_pattern = r'^/(?P<resource_name>%s)/?$' % resource_name
        detail_pattern = r'^/(?P<resource_name>%s)\((?P<%s>\w[\w/-]*)\)/?$' % (resource_name, detail_name)

        return patterns('',
            url(list_pattern, self.wrap_view('dispatch_list'), name='api_dispatch_list'),
            url(detail_pattern, self.wrap_view('dispatch_detail'), name='api_dispatch_detail')
        )

    def determine_format(self, request):
        """
        Used to determine the desired format.

        Largely relies on ``tastypie.utils.mime.determine_format`` but here
        as a point of extension.
        """
        return get_mime_format(request, self._meta.serializer, default_format=self._meta.default_format)

    def resource_uri_kwargs(self, bundle_or_obj=None):
        """
        Builds a dictionary of keyword arguments to help generate URIs.

        Automatically provides the OData resource name (and optionally the
        `Resource.Meta.api_name` if populated by an `Api` object).

        If the `bundle_or_obj` argument is provided, it calls
        `Resource.detail_uri_kwargs` for additional keyword arguments.
        """
        kwargs = {
            'resource_name': self.odata_resource_name
        }

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        if bundle_or_obj is not None:
            kwargs.update(self.detail_uri_kwargs(bundle_or_obj))

        return kwargs

    def obj_get_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.

        Takes an optional ``request`` object, whose ``GET`` dictionary can be
        used to narrow the query.
        """
        query_args = {}
        if hasattr(bundle.request, 'GET'):
            # We want a mutable `QueryDict`
            query_args = bundle.request.GET.copy()

        expression = self.build_filters(query_args)

        try:
            objects = self.get_object_list(bundle.request).filter(expression)
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest('Invalid resource lookup data provided (mismatched type).')

    def obj_get(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get``.

        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        try:
            object_list = self.get_object_list(bundle.request).filter(**kwargs)

            if len(object_list) != 1:
                class_name = self._meta.object_class.__name__
                stringified_kwargs = ', '.join(['%s=%s' % (key, value) for key, value in kwargs.items()])

                if len(object_list) <= 0:
                    raise self._meta.object_class.DoesNotExist('Couldn\'t find an instance of `%s` which matched `%s`.' % (class_name, stringified_kwargs))
                else:
                    raise MultipleObjectsReturned('More than `%s` matched `%s`.' % (class_name, stringified_kwargs))

            bundle.obj = object_list[0]
            self.authorized_read_detail(object_list, bundle)

            return bundle.obj
        except ValueError:
            raise NotFound('Invalid resource lookup data provided (mismatched type).')

    def check_filtering(self, field_name, filter_type='exact'):
        # FIXME: Check base class implementation for allowable fields.
        return self.fields[field_name].attribute

    def get_set_expression(self, query_args=None):
        filter_str = query_args.get('$set')

        if filter_str:
            filter_key = 'pk{0}in'.format(LOOKUP_SEP)
            # FIXME: We're being lazy right now with json.loads. Make this more robust.
            filter_value = json.loads(filter_str)
            return Q(**{filter_key: filter_value})

        return Q()

    def get_filter_expression(self, query_args=None):
        filter_str = query_args.get('$filter')

        if filter_str:
            return parse_filter(filter_str, self)

        return Q()

    def build_filters(self, query_args=None):
        return self.get_set_expression(query_args) & self.get_filter_expression(query_args)

    def serialize(self, request, data, format, options=None):
        """
        Given a request, data and a desired format, produces a serialized
        version suitable for transfer over the wire.

        Mostly a hook, this uses the ``Serializer`` from ``Resource._meta``.
        """
        return self._meta.serializer.serialize(data, format, options or {})
