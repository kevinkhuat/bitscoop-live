from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.views import APIView as TastyAPIView
from ografy.apps.tastydata.api import BaseApi


class APIEndpoints(TastyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'data': reverse('data-list', request=request, format=format),
            'event': reverse('event-list', request=request, format=format),
            'message': reverse('message-list', request=request, format=format),
            'settings': reverse('settings-list', request=request, format=format),
            'provider': reverse('provider-list', request=request, format=format),
            'signal': reverse('signal-list', request=request, format=format),
            'user': reverse('user-list', request=request, format=format),
        })


class DataView(TastyAPIView):
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.DataApi.get(
            val=BaseApi.query_by_user_id_request(request))
        data_list = list(get_query)
        return Response(self.serialize(data_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_data = self.deserialize(request.data)
        post_data.user_id = request.user.id

        data = obase_api.DataApi.post(
            data=post_data)
        return Response(self.serialize(data))


class DataSingleView(TastyAPIView):
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.DataApi.delete(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.DataApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_data = self.serialize(list(get_query))
        return Response(serial_data)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_data = self.deserialize(request.data)
        patch_data.user_id = request.user.id

        data = obase_api.DataApi.patch(
            val=pk,
            data=patch_data)
        return Response(self.serialize(data))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_data = self.deserialize(request.data)
        post_data.user_id = request.user.id

        data = obase_api.DataApi.put(
            pk=pk,
            data=post_data)
        return Response(self.serialize(data))


class EventView(TastyAPIView):
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.EventApi.get(
            val=BaseApi.query_by_user_id_request(request))
        event_list = list(get_query)
        return Response(self.serialize(event_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_event = self.deserialize(request.data)
        post_event.user_id = request.user.id

        event = obase_api.EventApi.post(
            data=post_event)
        return Response(self.serialize(event))


class EventSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.EventApi.delete(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.EventApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_event = self.serialize(list(get_query))
        return Response(serial_event)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_event = self.deserialize(request.data)
        patch_event.user_id = request.user.id

        event = obase_api.DataApi.patch(
            val=pk,
            data=patch_event)
        return Response(self.serialize(event))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_event = self.deserialize(request.data)
        put_event.user_id = request.user.id

        event = obase_api.EventApi.patch(
            val=pk,
            data=put_event)
        return Response(self.serialize(event))

    def data(self, request, pk, **kwargs):
        get_query = obase_api.DataApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_data = self.serialize(list(get_query))
        return Response(serial_data)


class MessageView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.MessageApi.get(
            val=BaseApi.query_by_user_id_request(request))
        message_list = list(get_query)
        return Response(self.serialize(message_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_message = self.deserialize(request.data)
        post_message.user_id = request.user.id

        message = obase_api.DataApi.post(
            data=post_message)
        return Response(self.serialize(message))


class MessageSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.MessageApi.delete(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.MessageApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_message = self.serialize(list(get_query))
        return Response(serial_message)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_message = self.deserialize(request.data)
        patch_message.user_id = request.user.id

        message = obase_api.DataApi.patch(
            val=pk,
            data=patch_message)
        return Response(self.serialize(message))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_data = self.deserialize(request.data)
        put_data.user_id = request.user.id

        message = obase_api.DataApi.put(
            pk=pk,
            data=put_data)
        return Response(self.serialize(message))

    def event(self, request, pk, **kwargs):
        get_query = obase_api.EventApi.get(
            val=BaseApi.query_by_user_id_request(request))
        event_list = list(get_query)
        return Response(self.serialize(event_list))

    def data(self, request, pk, **kwargs):
        get_query = obase_api.DataApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_data = self.serialize(list(get_query))
        return Response(serial_data)


class ProviderView(TastyAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.ProviderApi.get(
            val=BaseApi.query_by_user_id_request(request))
        provider_list = list(get_query)
        return Response(self.serialize(provider_list, many=True))


class ProviderSingleView(TastyAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.ProviderApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        provider = list(get_query)
        return Response(self.serialize(provider))


class SettingsView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SettingsApi.get(
            val=BaseApi.query_by_user_id_request(request))
        settings = list(get_query)
        return Response(self.serialize(settings))


class SettingsSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SettingsApi.get(
            val=BaseApi.query_by_user_id_request(request))
        settings = list(get_query)
        return Response(self.serialize(settings))

    # TODO: Replace with patch
    def post(self, request, format=None):
        # TODO: Better user filter
        post_settings = self.deserialize(request.data)
        post_settings.user = request.user

        settings = core_api.SettingsApi.post(
            data=post_settings)
        return Response(self.serialize(settings))


class SignalView(TastyAPIView):
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        request_user_query = BaseApi.query_by_user_id_request(request)
        get_query = core_api.SignalApi.get(
            val=request_user_query)
        signal_list = list(get_query)
        return Response(self.serialize(signal_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(request.data)
        post_signal.user = request.user

        signal = core_api.SignalApi.post(
            data=post_signal)
        return Response(self.serialize(signal))


class SignalSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        core_api.SignalApi.delete(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.SignalApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_signal = self.serialize(list(get_query))
        return Response(serial_signal)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_signal = self.deserialize(request.data)
        patch_signal.user = request.user

        data = core_api.SignalApi.patch(
            val=pk,
            data=patch_signal)
        return Response(self.serialize(data))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(request.data)
        post_signal.user = request.user

        signal = core_api.SignalApi.put(
            pk=pk,
            data=post_signal)
        return Response(self.serialize(signal))

    def provider(self, request, pk, **kwargs):
        get_query = core_api.ProviderApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        provider = list(get_query)
        return Response(self.serialize(provider))


class UserView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.UserApi.get(
            val=BaseApi.query_by_user_id_request(request))
        user_list = list(get_query)
        return Response(self.serialize(user_list, many=True))


class UserSingleView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.UserApi.get(
            val=BaseApi.query_by_user_id_request_pk(request, pk))
        serial_user = self.serialize(list(get_query))
        return Response(serial_user)

