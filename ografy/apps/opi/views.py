import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from social.apps.django_app.default.models import UserSocialAuth

import ografy.apps.opi.serializers as opi_serializer
from ografy.contrib.locationtoolbox import estimation
from ografy.contrib.pytoolbox import strip_invalid_key_characters
from ografy.contrib.tastydata.pagination import OgrafyItemPagination
from ografy.contrib.tastydata.views import DjangoAPIView, MongoAPIListView, MongoAPIView
from ografy.core import api as core_api
from ografy.core.documents import Settings


class APIEndpoints(DjangoAPIView):
    def get(self, request, format=None):
        return Response({
            'event': reverse('event-list', request=request, format=format),
            'contact': reverse('contact-list', request=request, format=format),
            'content': reverse('content-list', request=request, format=format),
            'location': reverse('location-list', request=request, format=format),
            'provider': reverse('provider-list', request=request, format=format),
            'signal': reverse('signal-list', request=request, format=format),
        })


class DataView(MongoAPIListView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'title')
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def get(self, request):
        #     data_query = core_api.DataApi.get(
        #         request.query_filter &
        #         request.auth_filter
        #     )
        #     paginated_data_list = self.Meta.list(self, data_query)
        #
        #     return paginated_data_list
        return Response('GET request invalid at this endpoint', status=400)

    def post(self, request):
        # TODO: Better user filter
        post_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_data.user_id = request.user.id

        existing_data = core_api.DataApi.get(MongoAPIView.Meta.Q(ografy_unique_id=post_data['ografy_unique_id']))
        data_exists = len(existing_data) > 0

        if not data_exists:
            data_query = core_api.DataApi.post(
                data=post_data
            )
            data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet)
            serialized_response = self.serialize(
                data_object,
                context={
                    'request': request
                }
            )

            return Response(serialized_response)
        else:
            serialized_response = self.serialize(
                existing_data.get(),
                context={
                    'request': request
                }
            )

            return Response(serialized_response)


class DataSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def get(self, request, pk, format=None):
        #     data_query = core_api.DataApi.get(
        #         request.auth_filter &
        #         MongoAPIView.Meta.Q(pk=pk)
        #     )
        #     data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        #     serialized_response = self.serialize(
        #         data_object,
        #         context={
        #             'request': request,
        #             'format': format
        #         }
        #     )
        #
        #     return Response(serialized_response)
        return Response('GET request invalid at this endpoint', status=400)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_data.user_id = request.user.id

        data_query = core_api.DataApi.patch(
            val=pk,
            data=patch_data
        )
        data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        put_data.user_id = request.user.id

        data_query = core_api.DataApi.put(
            pk=pk,
            data=put_data
        )
        data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class ContactView(MongoAPIListView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'title')
    serializer = opi_serializer.ContactSerializer
    serializer_class = opi_serializer.ContactSerializer

    def get(self, request):
        #     contact_query = core_api.ContactApi.get(
        #         request.query_filter &
        #         request.auth_filter
        #     )
        #     paginated_contact_list = self.Meta.list(self, contact_query)
        #
        #     return paginated_contact_list
        return Response('GET request invalid at this endpoint', status=400)

    def post(self, request):
        # TODO: Better user filter
        post_contact = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_contact.user_id = request.user.id

        existing_contact = core_api.ContactApi.get(MongoAPIView.Meta.Q(ografy_unique_id=post_contact['ografy_unique_id']))
        contact_exists = len(existing_contact) > 0

        if not contact_exists:
            contact_query = core_api.ContactApi.post(
                data=post_contact
            )
            contact_object = opi_serializer.evaluate(contact_query, self.Meta.QuerySet)
            serialized_response = self.serialize(
                contact_object,
                context={
                    'request': request
                }
            )

            return Response(serialized_response)
        else:
            serialized_response = self.serialize(
                existing_contact.get(),
                context={
                    'request': request
                }
            )

            return Response(serialized_response)


class ContactSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.ContactSerializer
    serializer_class = opi_serializer.ContactSerializer

    def get(self, request, pk, format=None):
        #     contact_query = core_api.ContactApi.get(
        #         request.auth_filter &
        #         MongoAPIView.Meta.Q(pk=pk)
        #     )
        #     contact_object = opi_serializer.evaluate(contact_query, self.Meta.QuerySet, many=False)
        #     serialized_response = self.serialize(
        #         contact_object,
        #         context={
        #             'request': request,
        #             'format': format
        #         }
        #     )
        #
        #     return Response(serialized_response)
        return Response('GET request invalid at this endpoint', status=400)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_contact = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_contact.user_id = request.user.id

        contact_query = core_api.ContactApi.patch(
            val=pk,
            data=patch_contact
        )
        contact_object = opi_serializer.evaluate(contact_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            contact_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        put_data.user_id = request.user.id

        contact_query = core_api.ContactApi.put(
            pk=pk,
            data=put_data
        )
        contact_object = opi_serializer.evaluate(contact_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            contact_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class ContentView(MongoAPIListView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.ContentSerializer
    serializer_class = opi_serializer.ContentSerializer

    def get(self, request):
        #     content_query = core_api.ContentApi.get(
        #         request.query_filter &
        #         request.auth_filter
        #     )
        #     paginated_content_list = self.Meta.list(self, content_query)
        #
        #     return paginated_content_list
        return Response('GET request invalid at this endpoint', status=400)

    def post(self, request):
        # TODO: Better user filter
        post_content = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_content.user_id = request.user.id

        existing_content = core_api.ContentApi.get(MongoAPIView.Meta.Q(ografy_unique_id=post_content['ografy_unique_id']))
        content_exists = len(existing_content) > 0

        if not content_exists:
            content_query = core_api.ContentApi.post(
                data=post_content
            )
            content_object = opi_serializer.evaluate(content_query, self.Meta.QuerySet)
            serialized_response = self.serialize(
                content_object,
                context={
                    'request': request
                }
            )

            return Response(serialized_response)
        else:
            serialized_response = self.serialize(
                existing_content.get(),
                context={
                    'request': request
                }
            )

            return Response(serialized_response)


class ContentSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.ContentSerializer
    serializer_class = opi_serializer.ContentSerializer

    def get(self, request, pk, format=None):
        #     content_query = core_api.ContentApi.get(
        #         request.auth_filter &
        #         MongoAPIView.Meta.Q(pk=pk)
        #     )
        #     content_object = opi_serializer.evaluate(content_query, self.Meta.QuerySet, many=False)
        #     serialized_response = self.serialize(
        #         content_object,
        #         context={
        #             'request': request,
        #             'format': format
        #         }
        #     )
        #
        #     return Response(serialized_response)
        return Response('GET request invalid at this endpoint', status=400)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_content = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_content.user_id = request.user.id

        content_query = core_api.ContentApi.patch(
            val=pk,
            data=patch_content
        )
        content_object = opi_serializer.evaluate(content_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            content_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        put_data.user_id = request.user.id

        content_query = core_api.ContentApi.put(
            pk=pk,
            data=put_data
        )
        content_object = opi_serializer.evaluate(content_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            content_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class EventView(MongoAPIListView):
    ordering_fields = ('provider_name', 'datetime', 'name', 'created', 'updated', 'user_id', 'signal')
    serializer = opi_serializer.EventSerializer
    serializer_class = opi_serializer.EventSerializer

    def get(self, request):
        # get_query = core_api.EventApi.get(
        #     request.query_filter &
        #     request.auth_filter
        # )
        # paginated_event_list = self.Meta.list(self, get_query)
        #
        # return paginated_event_list

        return Response('GET request invalid at this endpoint', status=400)

    # TODO: Add logic for for populating signal and prover from just signal id
    def post(self, request, format=None):
        # TODO: Better user filter
        post_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_event.user_id = request.user.id

        event_exists = len(core_api.EventApi.get(MongoAPIView.Meta.Q(ografy_unique_id=post_event['ografy_unique_id']))) > 0

        if not event_exists:
            if 'location' not in post_event.keys():
                post_event['location'] = estimation.estimate(post_event['user_id'], post_event['datetime'])

            event_query = core_api.EventApi.post(
                data=post_event
            )

            event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet)
            serialized_response = self.serialize(
                event_object,
                context={
                    'request': request,
                    'format': format
                }
            )

            return Response(serialized_response)
        else:
            return Response('Event exists', status=409)


class EventSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    serializer_class = opi_serializer.EventSerializer

    def delete(self, request, pk):
        core_api.EventApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        #     event_query = core_api.EventApi.get(
        #         request.auth_filter &
        #         MongoAPIView.Meta.Q(pk=pk)
        #     )
        #     event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet, many=False)
        #     serialized_response = self.serialize(
        #         event_object,
        #         context={
        #             'request': request,
        #             'format': format
        #         }
        #     )
        #
        #     return Response(serialized_response)
        return Response('GET request invalid at this endpoint', status=400)

    # TODO: Add logic for for populating signal and prover from just signal id
    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_event = self.deserialize(
            request.data,
            context={
                'request': request,
            }
        )
        patch_event.user_id = request.user.id

        event_query = core_api.EventApi.patch(
            val=pk,
            data=patch_event
        )
        event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    # TODO: Add logic for for populating signal and prover from just signal id
    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        put_event.user_id = request.user.id

        event_query = core_api.EventApi.patch(
            val=pk,
            data=put_event
        )
        event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class LocationView(MongoAPIListView):
    ordering_fields = ('browser')
    serializer = opi_serializer.LocationSerializer
    serializer_class = opi_serializer.LocationSerializer

    def get(self, request):
        #     get_query = core_api.LocationApi.get(
        #         request.query_filter &
        #         request.auth_filter
        #     )
        #     paginated_event_list = self.Meta.list(self, get_query)
        #
        #     return paginated_event_list
        return Response('GET request invalid at this endpoint', status=400)

    # TODO: Add logic for for populating signal and prover from just signal id
    def post(self, request, format=None):
        # TODO: Better user filter
        post_location = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_location['user_id'] = request.user.id

        event_query = core_api.LocationApi.post(
            data=post_location
        )
        ping_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            ping_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class ProviderView(MongoAPIListView):
    ordering_fields = ('id', 'name', 'backend_name')
    pagination_class = OgrafyItemPagination
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    def get(self, request, format=None):
        provider_query = core_api.ProviderApi.get(
            request.query_filter
        )
        paginated_data_list = self.Meta.list(self, provider_query)

        return paginated_data_list


class ProviderSingleView(MongoAPIView):
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    def get(self, request, pk, format=None):
        provider_query = core_api.ProviderApi.get(
            request.query_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(provider_query, self.Meta.QuerySet, many=False)

        return Response(self.serialize(
            provider_object,
            context={
                'request': request,
                'format': format
            }
        ))


class SignalView(MongoAPIListView):
    ordering_fields = ('id', 'user_id', 'provider', 'created')
    serializer = opi_serializer.SignalSerializer
    serializer_class = opi_serializer.SignalSerializer

    def get(self, request, format=None):
        get_query = core_api.SignalApi.get(
            request.query_filter &
            request.auth_filter
        )
        signal_list = opi_serializer.evaluate(get_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            signal_list,
            many=True,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_signal.user_id = request.user
        signal = core_api.SignalApi.post(
            data=post_signal
        )
        serialized_response = self.serialize(
            signal,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class SignalSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    serializer_class = opi_serializer.SignalSerializer

    def delete(self, request, pk):
        get_query = core_api.SignalApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        signal_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)

        usa_id = signal_object['usa_id']
        try:
            user_social_auth_object = UserSocialAuth.objects.get(user=request.user.id, id=usa_id)
            user_social_auth_object.delete()
        except ObjectDoesNotExist:
            pass

        core_api.SignalApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.SignalApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        signal_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            signal_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter

        patch_signal = self.deserialize(
            request.data,
            context={
                'request': request
            },
            partial=True
        )
        patch_signal.user_id = request.user

        data = core_api.SignalApi.patch(
            val=pk,
            data=patch_signal
        )
        serialized_response = self.serialize(
            data,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_signal.user_id = request.user

        signal = core_api.SignalApi.put(
            pk=pk,
            data=post_signal
        )
        serialized_response = self.serialize(
            signal,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def provider(self, request, pk, **kwargs):
        get_query = core_api.ProviderApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            provider_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class EstimateLocationView(MongoAPIView):
    def get(self, request, format=None):
        settings = Settings.objects.get(user_id=request.user.id)
        next_estimate_date = settings.last_estimate_all_locations + datetime.timedelta(days=5)
        new_estimate_allowed = datetime.datetime.now() > next_estimate_date

        if (new_estimate_allowed):
            estimation.reeestimate_all(request.user.id)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response('Re-estimation not allowed yet.', status=status.HTTP_400_BAD_REQUEST)


class SearchView(MongoAPIListView):
    ordering_fields = ('id', 'user_id', 'provider', 'created')
    serializer = opi_serializer.SearchSerializer
    serializer_class = opi_serializer.SearchSerializer

    def get(self, request, format=None):
        get_query = core_api.SearchApi.get(
            request.query_filter &
            request.auth_filter
        )
        search_list = opi_serializer.evaluate(get_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            search_list,
            many=True,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        stripped_data = strip_invalid_key_characters(request.data)
        post_search = self.deserialize(
            stripped_data,
            context={
                'request': request
            }
        )
        post_search.user_id = request.user
        search = core_api.SearchApi.post(
            data=post_search
        )
        serialized_response = self.serialize(
            search,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class SearchSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SearchSerializer
    serializer_class = opi_serializer.SearchSerializer

    def delete(self, request, pk):
        get_query = core_api.SearchApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        search_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)

        usa_id = search_object['usa_id']
        try:
            user_social_auth_object = UserSocialAuth.objects.get(user=request.user.id, id=usa_id)
            user_social_auth_object.delete()
        except ObjectDoesNotExist:
            pass

        core_api.SearchApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.SearchApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        search_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            search_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter

        patch_search = self.deserialize(
            request.data,
            context={
                'request': request
            },
            partial=True
        )
        patch_search.user_id = request.user

        data = core_api.SearchApi.patch(
            val=pk,
            data=patch_search
        )
        serialized_response = self.serialize(
            data,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_search = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_search.user_id = request.user

        search = core_api.SearchApi.put(
            pk=pk,
            data=post_search
        )
        serialized_response = self.serialize(
            search,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)
