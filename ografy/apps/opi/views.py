from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from social.apps.django_app.default.models import UserSocialAuth

import ografy.apps.opi.serializers as opi_serializer
from ografy.contrib.multiauth.decorators import login_required
from ografy.contrib.tastydata.pagination import OgrafyItemPagination
from ografy.contrib.tastydata.views import MongoAPIListView, MongoAPIView
from ografy.core import api as core_api


class ProviderView(MongoAPIListView):
    ordering_fields = ('id', 'name', 'backend_name')
    pagination_class = OgrafyItemPagination
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


class SignalView(MongoAPIListView):
    ordering_fields = ('id', 'user_id', 'provider', 'created')
    serializer = opi_serializer.SignalSerializer
    serializer_class = opi_serializer.SignalSerializer

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SignalView, self).dispatch(*args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SignalSingleView, self).dispatch(*args, **kwargs)

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
