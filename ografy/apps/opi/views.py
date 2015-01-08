from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.views import APIView as TastyAPIView


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
        get_query = obase_api.DataViewApi.user_get(request)
        data_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(data_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_data = self.deserialize(request.data)
        post_data.user_id = request.user.id

        data = obase_api.DataViewApi.post(data=post_data)
        return Response(self.serialize(data))


class DataSingleView(TastyAPIView):
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.DataViewApi.user_pk_delete(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.DataViewApi.user_pk_get(request, pk)
        data_object =opi_serializer.evaluate(get_query)
        return Response( self.serialize(data_object))

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_data = self.deserialize(request.data)
        patch_data.user_id = request.user.id

        data = obase_api.DataViewApi.patch(val=pk, data=patch_data)
        return Response(self.serialize(data))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_data = self.deserialize(request.data)
        post_data.user_id = request.user.id

        data = obase_api.DataViewApi.put(pk=pk, data=post_data)
        return Response(self.serialize(data))


class EventView(TastyAPIView):
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.EventViewApi.user_get(request)
        event_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(event_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_event = self.deserialize(request.data)
        post_event.user_id = request.user.id

        event = obase_api.EventViewApi.post(data=post_event)
        return Response(self.serialize(event))


class EventSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.EventViewApi.user_pk_delete(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.EventViewApi.user_get(request, pk)
        event_object = opi_serializer.evaluate(get_query)
        serial_event = self.serialize(event_object)
        return Response(serial_event)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_event = self.deserialize(request.data)
        patch_event.user_id = request.user.id

        event = obase_api.EventViewApi.patch(val=pk, data=patch_event)
        return Response(self.serialize(event))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_event = self.deserialize(request.data)
        put_event.user_id = request.user.id

        event = obase_api.EventViewApi.patch(val=pk, data=put_event)
        return Response(self.serialize(event))

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.DataViewApi.user_get(request, pk)
        data_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(data_object))


class MessageView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.MessageViewApi.user_get(request)
        message_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(message_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_message = self.deserialize(request.data)
        post_message.user_id = request.user.id

        message = obase_api.DataViewApi.post(data=post_message)
        return Response(self.serialize(message))


class MessageSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.MessageViewApi.user_pk_delete(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.MessageViewApi.user_get(request, pk)
        message_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(message_object))

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_message = self.deserialize(request.data)
        patch_message.user_id = request.user.id

        message = obase_api.MessageViewApi.patch(val=pk, data=patch_message)
        return Response(self.serialize(message))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        put_data = self.deserialize(request.data)
        put_data.user_id = request.user.id

        message = obase_api.MessageViewApi.put(pk=pk, data=put_data)
        return Response(self.serialize(message))

    def event(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.EventViewApi.user_pk_get(request, pk)
        event_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(event_object))

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.DataViewApi.user_pk_get(request, pk)
        data_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(data_object))


class ProviderView(TastyAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.ProviderViewApi.filter_get(request)
        provider_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(provider_list, many=True))


class ProviderSingleView(TastyAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.ProviderViewApi.get(pk)
        provider_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(provider_object))


class SettingsView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SettingsViewApi.user_get(request)
        settings_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(settings_list))


class SettingsSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SettingsViewApi.user_get(request)
        settings_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(settings_object))

    # TODO: Replace with patch
    def post(self, request, format=None):
        # TODO: Better user filter
        post_settings = self.deserialize(request.data)
        post_settings.user = request.user

        settings = core_api.SettingsViewApi.post(data=post_settings)
        return Response(self.serialize(settings))


class SignalView(TastyAPIView):
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SignalViewApi.user_get(request)
        signal_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(signal_list, many=True))

    def post(self, request, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(request.data)
        post_signal.user = request.user

        signal = core_api.SignalViewApi.post(data=post_signal)
        return Response(self.serialize(signal))


class SignalSingleView(TastyAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        core_api.SignalViewApi.user_pk_delete(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.SignalViewApi.user_get(request, pk)
        signal_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(signal_object))

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_signal = self.deserialize(request.data)
        patch_signal.user = request.user

        data = core_api.SignalViewApi.patch(val=pk, data=patch_signal)
        return Response(self.serialize(data))

    def put(self, request, pk, format=None):
        # TODO: Better user filter
        post_signal = self.deserialize(request.data)
        post_signal.user = request.user

        signal = core_api.SignalViewApi.put(pk=pk, data=post_signal)
        return Response(self.serialize(signal))

    def provider(self, request, pk, **kwargs):
        get_query = core_api.ProviderViewApi.user_pk_get(request, pk)
        provider_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(provider_object))


class UserView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.UserViewApi.user_get(request)
        user_list = opi_serializer.evaluate(get_query)
        return Response(self.serialize(user_list, many=True))


class UserSingleView(TastyAPIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.UserViewApi.user_pk_get(request, pk)
        user_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(user_object))

