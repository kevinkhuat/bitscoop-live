from rest_framework import permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.core import api as core_api
from ografy.apps.obase import api as obase_api
from ografy.apps.tastydata.pagination import TwentyItemPagination, OneHundredItemPagination, FiveHundredItemPagination
from ografy.apps.tastydata.views import DjangoAPIView, MongoAPIView

class ListMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(request)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class NewListAPIView(ListMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class APIEndpoints(DjangoAPIView):
    permission_classes = (permissions.IsAuthenticated,)

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


class DataView(MongoAPIView, NewListAPIView):
    filter_backends = (OrderingFilter,)
    ordering = 'created'
    ordering_fields = ('user', 'created', 'updated')
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = TwentyItemPagination
    serializer = opi_serializer.DataSerializer
    serializer_class = opi_serializer.DataSerializer

    def get(self, request):
        get_query = obase_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        data_list = opi_serializer.evaluate(get_query)
        paginated_data_list = NewListAPIView.list(self, data_list)
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

    def delete(self, request, pk):
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
        data = obase_api.DataApi.patch(
            val=pk,
            data=patch_data
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
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class EventView(MongoAPIView, NewListAPIView):
    filter_backends = (OrderingFilter,)
    ordering = 'datetime'
    ordering_fields = ('provider_name', 'datetime', 'name')
    pagination_class = TwentyItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.EventSerializer
    serializer_class = opi_serializer.EventSerializer

    def get(self, request):
        get_query = obase_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        event_list = opi_serializer.evaluate(get_query)
        paginated_event_list = NewListAPIView.list(self, event_list)
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

        event = obase_api.EventApi.post(
            data=post_event
        )
        serialized_response = self.serialize(
            event,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class EventSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk):
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

        event = obase_api.EventApi.patch(
            val=pk,
            data=patch_event
        )
        serialized_response = self.serialize(
            event,
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

        event = obase_api.EventApi.patch(
            val=pk,
            data=put_event
        )
        serialized_response = self.serialize(
            event,
            context={
                'request': request,
                'format': format
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

class MessageView(MongoAPIView, ListMixin):
    # TODO: Check user association on any updates & add access permissions
    filter_backends = (OrderingFilter,)
    ordering = 'id'
    ordering_fields = ('id', 'message_to', 'message_from', 'message_body')
    pagination_class = TwentyItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.MessageSerializer
    serializer_class = opi_serializer.MessageSerializer

    def get(self, request):
        get_query = obase_api.EventApi.get(
            request.query_filter &
            request.auth_filter
        )
        message_list = opi_serializer.evaluate(get_query)
        paginated_message_list = NewListAPIView.list(self, message_list)
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

    def delete(self, request, pk):
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

        message = obase_api.MessageApi.patch(
            val=pk,
            data=patch_message
        )
        serialized_response = self.serialize(
            message,
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

        message = obase_api.MessageApi.put(
            pk=pk,
            data=put_data
        )
        serialized_response = self.serialize(
            message,
            context={
                'request': request,
                'format': format
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
    filter_backends = (OrderingFilter,)
    ordering = 'id'
    ordering_fields = ('id', 'name', 'backend_name')
    pagination_class = FiveHundredItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    def get(self, request, format=None):
        get_query = core_api.ProviderApi.get(
            request.query_filter
        )
        provider_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            provider_list,
            many=True,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class ProviderSingleView(DjangoAPIView):
    serializer = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        get_query = core_api.ProviderApi.get(
            request.auth_filter &
            DjangoAPIView.Meta.Q(pk=pk)
        )
        provider_object = opi_serializer.evaluate(get_query)
        return Response(self.serialize(
            provider_object,
            context={
                'request': request,
                'format': format
            }
        ))


class SettingsView(MongoAPIView):
    # TODO: Restrict to admins or remove?
    filter_backends = (OrderingFilter,)
    ordering = 'id'
    ordering_fields = ('id', 'message_to', 'message_from', 'message_body')
    pagination_class = OneHundredItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.SettingsSerializer
    serializer_class = opi_serializer.SettingsSerializer

    def get(self, request, format=None):
        get_query = core_api.SignalApi.get(
            request.query_filter &
            request.auth_filter
        )
        settings_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            settings_list,
            context={
                'request': request,
                'format': format
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

        settings = core_api.SignalApi.post(
            data=post_settings
        )
        serialized_response = self.serialize(
            settings,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class SignalView(DjangoAPIView):
    filter_backends = (OrderingFilter,)
    ordering = 'id'
    ordering_fields = ('id', 'user', 'provider', 'created')
    pagination_class = TwentyItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.SignalSerializer
    serializer_class = opi_serializer.SignalSerializer

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
    permission_classes = (permissions.IsAuthenticated,)

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
        signal_object = opi_serializer.evaluate(get_query)
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
        provider_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            provider_object,
            context={
                'request': request
            }
        )

        return Response(serialized_response)


class UserView(DjangoAPIView):
    filter_backends = (OrderingFilter,)
    ordering = 'id'
    ordering_fields = ('id', 'email', 'handle', 'date_joined')
    pagination_class = TwentyItemPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer = opi_serializer.UserSerializer
    serializer_class = opi_serializer.UserSerializer

    def get(self, request, format=None):
        get_query = core_api.UserApi.get(
            request.query_filter
        )
        user_list = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            user_list,
            many=True,
            context={
                'request': request,
                'format': format
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
        )
        user_object = opi_serializer.evaluate(get_query)
        serialized_response = self.serialize(
            user_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

