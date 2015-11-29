from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from social.apps.django_app.default.models import UserSocialAuth

import server.apps.opi.serializers as opi_serializer
from server.contrib.multiauth.decorators import login_required
from server.contrib.tastydata.pagination import BitscoopItemPagination
from server.contrib.tastydata.views import MongoAPIListView, MongoAPIView
from server.core import api as core_api


class ProviderView(MongoAPIListView):
    ordering_fields = ('id', 'name', 'backend_name')
    pagination_class = BitscoopItemPagination
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProviderView, self).dispatch(*args, **kwargs)

    def get(self, request, format=None):
        provider_query = core_api.ProviderApi.get(
            request.query_filter
        )
        paginated_data_list = self.Meta.list(self, provider_query)

        return paginated_data_list


class ProviderSingleView(MongoAPIView):
    serializer = opi_serializer.ProviderSerializer
    serializer_class = opi_serializer.ProviderSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProviderSingleView, self).dispatch(*args, **kwargs)

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


class ConnectionView(MongoAPIListView):
    ordering_fields = ('id', 'user_id', 'provider', 'created')
    serializer = opi_serializer.ConnectionSerializer
    serializer_class = opi_serializer.ConnectionSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConnectionView, self).dispatch(*args, **kwargs)

    def get(self, request, format=None):
        get_query = core_api.ConnectionApi.get(
            request.query_filter &
            request.auth_filter
        )
        connection_list = opi_serializer.evaluate(get_query, self.Meta.QuerySet)
        serialized_response = self.serialize(
            connection_list,
            many=True,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def post(self, request, format=None):
        # TODO: Better user filter
        post_connection = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_connection.user_id = request.user
        connection = core_api.ConnectionApi.post(
            data=post_connection
        )
        serialized_response = self.serialize(
            connection,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)


class ConnectionSingleView(MongoAPIView):
    # TODO: Check user association on any updates & add access permissions
    serializer = opi_serializer.ConnectionSerializer
    serializer_class = opi_serializer.ConnectionSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConnectionSingleView, self).dispatch(*args, **kwargs)

    def delete(self, request, pk):
        get_query = core_api.ConnectionApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        connection_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)

        usa_id = connection_object['usa_id']
        try:
            user_social_auth_object = UserSocialAuth.objects.get(user=request.user.id, id=usa_id)
            user_social_auth_object.delete()
        except ObjectDoesNotExist:
            pass

        core_api.ConnectionApi.delete(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        get_query = core_api.ConnectionApi.get(
            request.auth_filter &
            MongoAPIView.Meta.Q(pk=pk)
        )
        connection_object = opi_serializer.evaluate(get_query, self.Meta.QuerySet, many=False)
        serialized_response = self.serialize(
            connection_object,
            context={
                'request': request,
                'format': format
            }
        )

        return Response(serialized_response)

    def patch(self, request, pk, format=None):
        # TODO: Better user filter

        patch_connection = self.deserialize(
            request.data,
            context={
                'request': request
            },
            partial=True
        )
        patch_connection.user_id = request.user

        data = core_api.ConnectionApi.patch(
            val=pk,
            data=patch_connection
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
        post_connection = self.deserialize(
            request.data,
            context={
                'request': request
            }
        )
        post_connection.user_id = request.user

        connection = core_api.ConnectionApi.put(
            pk=pk,
            data=post_connection
        )
        serialized_response = self.serialize(
            connection,
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
