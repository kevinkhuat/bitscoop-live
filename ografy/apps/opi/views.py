from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.pagination import OgrafyItemPagination
from ografy.apps.tastydata.views import DjangoAPIView, DjangoAPIListView, MongoAPIView, MongoAPIListView


class APIEndpoints(DjangoAPIView):

    def get(self, request, format=None):
        return Response({
            'data': reverse('data-list', request=request, format=format),
            'event': reverse('event-list', request=request, format=format),
            'message': reverse('message-list', request=request, format=format),
            'provider': reverse('provider-list', request=request, format=format),
            'settings': reverse('settings-list', request=request, format=format),
            'signal': reverse('signal-list', request=request, format=format),
            'user': reverse('user-list', request=request, format=format),
        })


class DataView(MongoAPIListView):
    ordering_fields = ('user', 'created', 'updated')
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def get(self, request):
        data_query = obase_api.DataApi.get(
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
        post_data.user_id = request.user.id
        data_query = obase_api.DataApi.post(
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
        obase_api.DataApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        data_query = obase_api.DataApi.get(
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
        data_query = obase_api.DataApi.patch(
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
        data_query = obase_api.DataApi.put(
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
    ordering_fields = ('provider_name', 'datetime', 'name', 'created', 'updated', 'user_id', 'signal_id')
    serializer = opi_serializer.EventSerializer
    serializer_class = opi_serializer.EventSerializer

    def get(self, request):
        get_query = obase_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_event_list = self.Meta.list(self, get_query)
        return paginated_event_list

    def post(self, request, format=None):
        # TODO: Better user filter
        post_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_event.user_id = request.user.id

        event_query = obase_api.EventApi.post(
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
        obase_api.EventApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        event_query = obase_api.EventApi.get(
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

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_event = self.deserialize(
            request.data,
            context={
                'request': request,
            }
        )
        patch_event.user_id = request.user.id

        event_query = obase_api.EventApi.patch(
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

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        put_event.user_id = request.user.id

        event_query = obase_api.EventApi.patch(
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

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        data_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class MessageView(EventView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'message_to', 'message_from', 'message_body')
    serializer = opi_serializer.MessageSerializer
    serializer_class = opi_serializer.MessageSerializer

    def get(self, request):
        message_query = obase_api.MessageApi.get(
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
        message_query = obase_api.MessageApi.post(
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


class MessageSingleView(EventSingleView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    serializer_class = opi_serializer.MessageSerializer

    def delete(self, request, pk):
        obase_api.MessageApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        message_query = obase_api.MessageApi.get(
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

        message_query = obase_api.MessageApi.patch(
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

        message_query = obase_api.MessageApi.put(
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

    def event(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        event_query = obase_api.MessageApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        data_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class PlayView(EventView):
    # TODO: Check user association on any updates & add access permissions
    ordering_fields = ('id', 'title')
    serializer = opi_serializer.PlaySerializer
    serializer_class = opi_serializer.PlaySerializer

    def get(self, request):
        play_query = obase_api.PlayApi.get(
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
        play_query = obase_api.PlayApi.post(
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


class PlaySingleView(EventSingleView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.PlaySerializer
    serializer_class = opi_serializer.PlaySerializer

    def delete(self, request, pk):
        obase_api.PlayApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        play_query = obase_api.PlayApi.get(
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

        play_query = obase_api.PlayApi.patch(
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

        play_query = obase_api.PlayApi.put(
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

    def event(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        event_query = obase_api.PlayApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        event_object = opi_serializer.evaluate(event_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        data_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(data_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class ProviderView(DjangoAPIListView):
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


class ProviderSingleView(DjangoAPIView):
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    def get(self, request, pk, format=None):
        provider_query = core_api.ProviderApi.get(
            request.query_filter &
            DjangoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(provider_query, self.Meta.QuerySet, many=False)
        return Response(self.serialize(
            provider_object,
            context={
                'request': request,
                'format': format
            }
        ))


class SettingsView(MongoAPIListView):
    # TODO: Restrict to admins or remove?
    ordering = 'id'
    ordering_fields = ('id', 'user', 'created', 'updated')
    pagination_class = OgrafyItemPagination
    serializer = opi_serializer.SettingsSerializer
    serializer_class = opi_serializer.SettingsSerializer

    def get(self, request, format=None):
        settings_query = core_api.SettingsApi.get(
            request.query_filter &
            request.auth_filter
        )
        paginated_data_list = self.Meta.list(self, settings_query)
        return paginated_data_list


class SettingsSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SettingsSerializer
    serializer_class = opi_serializer.SettingsSerializer

    def get(self, request, pk, format=None):
        settings_query = core_api.SettingsApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        settings_object = opi_serializer.evaluate(settings_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            settings_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    # TODO: Replace with patch
    def post(self, request, format=None):
        # TODO: Better user filter
        post_settings = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_settings.user = request.user

        settings_query = core_api.SettingsApi.post(
            data=post_settings
        )
        settings_object = opi_serializer.evaluate(settings_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            settings_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class SignalView(DjangoAPIListView):
    ordering_fields = ('id', 'user', 'provider', 'created')
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
        post_signal.user = request.user
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


class SignalSingleView(DjangoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    serializer_class = opi_serializer.SignalSerializer

    def delete(self, request, pk):
        core_api.SignalApi.delete(
            request.auth_filter &
            DjangoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.SignalApi.get(
            request.auth_filter &
            DjangoAPIView.Meta.Q(pk=pk)
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
            }
        )
        patch_signal.user = request.user

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
        post_signal.user = request.user

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
            DjangoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            provider_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class UserView(DjangoAPIListView):
    ordering_fields = ('id', 'email', 'handle', 'date_joined')
    serializer = opi_serializer.UserSerializer
    serializer_class = opi_serializer.UserSerializer

    def get(self, request, format=None):
        get_query = core_api.UserApi.get(
            request.query_filter
        )
        user_list = opi_serializer.evaluate(get_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            user_list,
            many=True,
            context={
                'request': request,
                'formatrequest': format
            }
        )

        return Response(serialized_response)


class UserSingleView(DjangoAPIView):
    # TODO: Restrict to admins or remove?
    serializer = opi_serializer.UserSerializer
    serializer_class = opi_serializer.UserSerializer

    def get(self, request, pk, format=None):
        get_query = core_api.UserApi.get(
            val=pk
        )
        user_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            user_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)
