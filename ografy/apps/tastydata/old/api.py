from django.conf.urls import include, patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
import tastypie.fields
from tastypie.api import Api as BaseApi
from tastypie.utils.mime import determine_format, build_content_type

from ografy.apps.tastydata.serializers import Serializer


class Api(BaseApi):
    def __init__(self, serializer_class=Serializer, *args, **kwargs):
        super(Api, self).__init__(serializer_class=serializer_class, *args, **kwargs)

    @property
    def urls(self):
        """
        Provides URLconf details for the ``Api`` and all registered
        ``Resources`` beneath it.
        """

        top_level_pattern = r'^/(?P<api_name>%s)/?$' % self.api_name
        metadata_pattern = r'^/(?P<api_name>%s)/\$metadata/?$' % self.api_name

        pattern_list = [
            url(top_level_pattern, self.wrap_view('top_level'), name='api_%s_top_level' % self.api_name),
            url(metadata_pattern, self.wrap_view('metadata'), name='api_%s_metadata' % self.api_name),
        ]

        for name in sorted(self._registry.keys()):
            self._registry[name].api_name = self.api_name
            pattern_list.append(url(r'^/(?P<api_name>%s)' % self.api_name, include(self._registry[name].urls)))

        return patterns('', *pattern_list)

    def top_level(self, request, api_name=None):
        if api_name is None:
            api_name = self.api_name

        metadata_url = reverse('api_%s_metadata' % self.api_name, kwargs={
            'api_name': api_name,
        })

        return HttpResponsePermanentRedirect(metadata_url)

    def metadata(self, request, api_name=None):
        """
        A view that returns a serialized list of all resources registers
        to the ``Api``. Useful for discovery.
        """

        if api_name is None:
            api_name = self.api_name

        resources = {}

        for name in self._registry.keys():
            resource = self._registry[name]
            resource_class_name = resource.__class__.__name__
            resource_name = resource.odata_resource_name
            resource_uri = self._build_reverse_url('api_dispatch_list', kwargs={
                'api_name': api_name,
                'resource_name': resource_name,
            })

            properties = {}
            associations = {}

            for field_name in resource.fields.keys():
                field = resource.fields[field_name]
                if isinstance(field, tastypie.fields.RelatedField):
                    many = getattr(field, 'is_m2m', False)
                    data = {
                        'many': many,
                        'to': field.to_class.__name__,
                    }

                    if not many:
                        data['nullable'] = field.null

                    associations[field_name] = data
                else:
                    properties[field_name] = {
                        'type': field.dehydrated_type,
                        'nullable': not field.blank,
                        'readonly': field.readonly,
                    }

            resources[resource_class_name] = {
                'resource_name': resource_name,
                'resource_uri': resource_uri,
                'key': resource.primary_key_name,
                'properties': properties,
                'associations': associations,
            }

        desired_format = determine_format(request, self.serializer)
        serialized = self.serializer.serialize(resources, desired_format)

        return HttpResponse(content=serialized, content_type=build_content_type(desired_format))
