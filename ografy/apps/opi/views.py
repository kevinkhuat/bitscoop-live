from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.views import APIView


class APIEndpoints(APIView):
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


class DataView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        data_list = list(obase_api.DataApi.get())
        return Response(self.serialize(data_list, many=True))

    def post(self, request, format=None):
        data = obase_api.DataApi.post(data=self.deserialize(request.data))
        return Response(self.serialize(data))


class DataSingleView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.DataApi.delete(val=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        data = obase_api.DataApi.get(val=pk)
        return Response(self.serialize(data))

    def patch(self, request, pk, format=None):
        data = obase_api.DataApi.patch(val=pk, data=self.deserialize(request.data))
        return Response(self.serialize(data))

    def put(self, request, pk, format=None):
        data = obase_api.DataApi.put(pk=pk, data=self.deserialize(request.data))
        return Response(self.serialize(data))


class EventView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        events = list(obase_api.EventApi.get())
        return Response(self.serialize(events, many=True))

    def post(self, request, format=None):
        event = obase_api.EventApi.post(data=self.deserialize(request.data))
        return Response(self.serialize(event))


class EventSingleView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.EventApi.delete(val=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        event = list(obase_api.EventApi.get(val=pk))
        return Response(self.serialize(event))

    def patch(self, request, pk, format=None):
        event = obase_api.EventApi.patch(val=pk, data=self.deserialize(request.data))
        return Response(self.serialize(event))

    def put(self, request, pk, format=None):
        event = obase_api.EventApi.put(pk=pk, data=self.deserialize(request.data))
        return Response(self.serialize(event))

    def data(self, request, pk, **kwargs):
        event = obase_api.EventApi.get(val=pk)
        return Response(opi_serializer.DataSerializer().to_internal_value(event.data))


class MessageView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        messages = list(obase_api.MessageApi.get())
        return Response(self.serialize(messages, many=True))

    def post(self, request, format=None):
        message = obase_api.MessageApi.post(data=self.deserialize(request.data))
        return Response(self.serialize(message))


class MessageSingleView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.MessageApi.delete(val=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        message = list(obase_api.MessageApi.get(val=pk))
        return Response(self.serialize(message))

    def patch(self, request, pk, format=None):
        message = obase_api.MessageApi.patch(val=pk, data=self.deserialize(request.data))
        return Response(self.serialize(message))

    def put(self, request, pk, format=None):
        message = obase_api.MessageApi.put(pk=pk, data=self.deserialize(request.data))
        return Response(self.serialize(message))

    def event(self, request, pk, **kwargs):
        message = obase_api.MessageApi.get(val=pk)
        return Response(opi_serializer.EventSerializer().to_internal_value(message.event))

    def data(self, request, pk, **kwargs):
        message = obase_api.MessageApi.get(val=pk)
        return Response(opi_serializer.DataSerializer().to_internal_value(message.event.data))


class ProviderView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        providers = list(core_api.ProviderApi.get())
        return Response(self.serialize(providers, many=True))


class ProviderSingleView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        provider = list(core_api.ProviderApi.get(val=pk))
        return Response(self.serialize(provider))


class SignalView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        signals = list(core_api.SignalApi.get())
        return Response(self.serialize(signals, many=True))

    def post(self, request, format=None):
        signal = core_api.SignalApi.post(data=self.deserialize(request.data))
        return Response(self.serialize(signal))


class SettingsView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        settings_list = list(core_api.SettingsApi.get())
        return Response(self.serialize(settings_list, many=True))


class SettingsSingleView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        settings = list(core_api.SettingsApi.get())
        return Response(self.serialize(settings, many=True))

    # TODO: Replace with patch
    def post(self, request, format=None):
        settings = core_api.SettingsApi.post(data=self.deserialize(request.data))
        return Response(self.serialize(settings))


class SignalSingleView(APIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        core_api.SignalApi.delete(val=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        signal = list(core_api.SignalApi.get(val=pk))
        return Response(self.serialize(signal))

    def patch(self, request, pk, format=None):
        signal = core_api.SignalApi.patch(val=pk, data=self.deserialize(request.data))
        return Response(self.serialize(signal))

    def put(self, request, pk, format=None):
        signal = core_api.SignalApi.put(pk=pk, data=self.deserialize(request.data))
        return Response(self.serialize(signal))

    def provider(self, request, pk, **kwargs):
        signal = core_api.SignalApi.get(val=pk)
        return Response(opi_serializer.ProviderSerializer().to_internal_value(signal.provider))


class UserView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = list(core_api.UserApi.get())
        return Response(self.serialize(user, many=True))


class UserSingleView(APIView):
    # TODO: add access permissions
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        user = list(core_api.UserApi.get(val=pk))
        return Response(self.serialize(user))
