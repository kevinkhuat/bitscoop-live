from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.views import DjangoAPIView, MongoAPIView


class APIEndpoints(DjangoAPIView):
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


class DataView(MongoAPIView):
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.DataApi.get(
            request.query_filter &
            request.auth_filter
        )
        data_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            data_list,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        post_data = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_data.user_id = request.user.id
        data = obase_api.DataApi.post(
            data=post_data
        )
        serialized_response = self.serialize(
            data,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class DataSingleView(MongoAPIView):
    serializer = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.DataApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
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
        data = obase_api.DataApi.patch(
            val=pk,
            data=patch_data
        )
        serialized_response = self.serialize(
            data,
            context={
                'request': request
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
        data = obase_api.DataApi.put(
            pk=pk,
            data=post_data
        )
        serialized_response = self.serialize(
            data,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class EventView(MongoAPIView):
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        event_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            event_list,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        post_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_event.user_id = request.user.id

        event = obase_api.EventApi.post(
            data=post_event
        )
        serialized_response = self.serialize(
            event,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class EventSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.EventApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.EventApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        event_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter
        patch_event = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        patch_event.user_id = request.user.id

        event = obase_api.EventApi.patch(
            val=pk,
            data=patch_event
        )
        serialized_response = self.serialize(
            event,
            context={
                'request': request
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

        event = obase_api.EventApi.patch(
            val=pk,
            data=put_event
        )
        serialized_response = self.serialize(
            event,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class MessageView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = obase_api.MessageApi.get(
            request.query_filter &
            request.auth_filter
        )
        message_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            message_list,
            context={
                'request': request
            },
            many=True
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        post_message = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_message.user_id = request.user.id
        message = obase_api.MessageApi.post(
            data=post_message
        )
        serialized_response = self.serialize(
            message,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class MessageSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        obase_api.MessageApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = obase_api.MessageApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        message_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            message_object,
            context={
                'request': request}
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

        message = obase_api.MessageApi.patch(
            val=pk,
            data=patch_message
        )
        serialized_response = self.serialize(
            message,
            context={
                'request': request
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

        message = obase_api.MessageApi.put(
            pk=pk,
            data=put_data
        )
        serialized_response = self.serialize(
            message,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def event(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.EventApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        event_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            event_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

    def data(self, request, pk, **kwargs):
        # TODO: get pk to make work right
        get_query = obase_api.DataApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        data_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            data_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class ProviderView(DjangoAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.ProviderApi.get(
            request.query_filter &
            request.auth_filter
        )
        provider_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            provider_list,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class ProviderSingleView(DjangoAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.ProviderApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(provider_object, context={'request': request}))


class SettingsView(MongoAPIView):
    # TODO: Restrict to admins or remove?
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SignalApi.get(
            request.query_filter &
            request.auth_filter
        )
        settings_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            settings_list,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class SettingsSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SignalApi.get(
            request.query_filter &
            request.auth_filter
        )
        settings_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            settings_object,
            context={
                'request': request
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

        settings = core_api.SignalApi.post(
            data=post_settings
        )
        serialized_response = self.serialize(
            settings,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class SignalView(DjangoAPIView):
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.SignalApi.get(
            request.query_filter &
            request.auth_filter
        )
        signal_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            signal_list,
            many=True,
            context={
                'request': request
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
                'request': request
            }
        )

        return Response(serialized_response)


class SignalSingleView(DjangoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
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
        signal_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            signal_object,
            context={
                'request': request
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
                'request': request
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
                'request': request
            }
        )

        return Response(serialized_response)

    def provider(self, request, pk, **kwargs):
        get_query = core_api.ProviderApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            provider_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class UserView(DjangoAPIView):
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        get_query = core_api.UserApi.get(
            request.auth_filter
        )
        user_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            user_list,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class UserSingleView(DjangoAPIView):
    # TODO: Restrict to admins or remove?
    serializer = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.UserApi.get(
            val=pk
            # request.auth_filter &
            # MongoAPIView.Meta.Q(pk=pk)
        )
        user_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            user_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)

