import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from social.apps.django_app.default.models import UserSocialAuth

import ografy.apps.opi.serializers as opi_serializer
from ografy.contrib.locationtoolbox import estimation
from ografy.contrib.tastydata.pagination import OgrafyItemPagination
from ografy.contrib.tastydata.views import DjangoAPIView, MongoAPIListView, MongoAPIView
from ografy.core import api as core_api
from ografy.core.documents import Settings


class APIEndpoints(DjangoAPIView):

    def get(self, request, format=None):
        return Response({
            'data': reverse('data-list', request=request, format=format),
            'event': reverse('event-list', request=request, format=format),
            'message': reverse('message-list', request=request, format=format),
            'provider': reverse('provider-list', request=request, format=format),
            'settings': reverse('settings-list', request=request, format=format),
            'signal': reverse('signal-list', request=request, format=format),
            'user_id': reverse('user-list', request=request, format=format),
        })


class DataView(MongoAPIListView):
    ordering_fields = ('user_id', 'created', 'updated')
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def get(self, request):
        data_query = core_api.DataApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_data_list = self.Meta.list(self, data_query)

        return paginated_data_list

    def post(self, request):
        # TODO: Better user filter
        post_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_data['user_id'] = request.user.id
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


class DataSingleView(MongoAPIView):
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def delete(self, request, pk):
        core_api.DataApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        data_query = core_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
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
        post_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_data.user_id = request.user.id
        data_query = core_api.DataApi.put(
            pk=pk,
            data=post_data
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


class EventView(MongoAPIListView):
    ordering_fields = ('provider_name', 'datetime', 'name', 'created', 'updated', 'user_id', 'signal')
    serializer = opi_serializer.EventSerializer
    serializer_class = opi_serializer.EventSerializer

    def get(self, request):
        get_query = core_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_event_list = self.Meta.list(self, get_query)

        return paginated_event_list

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

        if post_event['location']['geolocation'] is None:
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
        event_query = core_api.EventApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
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
        get_query = core_api.LocationApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_event_list = self.Meta.list(self, get_query)

        return paginated_event_list

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


class MessageView(MongoAPIListView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'message_to', 'message_from', 'message_body')
    serializer = opi_serializer.MessageSerializer
    serializer_class = opi_serializer.MessageSerializer

    def get(self, request):
        message_query = core_api.MessageApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_message_list = self.Meta.list(self, message_query)

        return paginated_message_list

    def post(self, request):
        # TODO: Better user filter
        post_message = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_message.user_id = request.user.id
        message_query = core_api.MessageApi.post(
            data=post_message
        )
        message_object = opi_serializer.evaluate(message_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            message_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class MessageSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    serializer_class = opi_serializer.MessageSerializer

    def get(self, request, pk, format=None):
        message_query = core_api.MessageApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        message_object = opi_serializer.evaluate(message_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            message_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_message = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_message.user_id = request.user.id

        message_query = core_api.MessageApi.patch(
            val=pk,
            data=patch_message
        )
        message_object = opi_serializer.evaluate(message_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            message_object,
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

        message_query = core_api.MessageApi.put(
            pk=pk,
            data=put_data
        )
        message_object = opi_serializer.evaluate(message_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            message_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class PlayView(MongoAPIListView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'title')
    serializer = opi_serializer.PlaySerializer
    serializer_class = opi_serializer.PlaySerializer

    def get(self, request):
        play_query = core_api.PlayApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_play_list = self.Meta.list(self, play_query)

        return paginated_play_list

    def post(self, request):
        # TODO: Better user filter
        post_play = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_play.user_id = request.user.id
        play_query = core_api.PlayApi.post(
            data=post_play
        )
        play_object = opi_serializer.evaluate(play_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            play_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class PlaySingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.PlaySerializer
    serializer_class = opi_serializer.PlaySerializer

    def get(self, request, pk, format=None):
        play_query = core_api.PlayApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        play_object = opi_serializer.evaluate(play_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            play_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_play = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_play.user_id = request.user.id

        play_query = core_api.PlayApi.patch(
            val=pk,
            data=patch_play
        )
        play_object = opi_serializer.evaluate(play_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            play_object,
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

        play_query = core_api.PlayApi.put(
            pk=pk,
            data=put_data
        )
        play_object = opi_serializer.evaluate(play_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            play_object,
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


class PermissionView(MongoAPIListView):
    ordering_fields = ('provider', 'name')
    pagination_class = OgrafyItemPagination
    serializer = opi_serializer.PermissionSerializer
    serializer_class = opi_serializer.PermissionSerializer

    def get(self, request, format=None):
        provider_query = core_api.PermissionApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_data_list = self.Meta.list(self, provider_query)

        return paginated_data_list


class PermissionSingleView(MongoAPIView):
    serializer = opi_serializer.PermissionSerializer
    serializer_class = opi_serializer.PermissionSerializer

    def get(self, request, pk, format=None):
        provider_query = core_api.PermissionApi.get(
            request.auth_filter &
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
        user_social_auth_object = UserSocialAuth.objects.get(user=request.user.id, id=usa_id)
        user_social_auth_object.delete()

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
