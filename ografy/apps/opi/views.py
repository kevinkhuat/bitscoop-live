from django.views.generic import View
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.tastydata.mongo_rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.opi.permissions import IsUser
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.core.documents import Settings


# TODO: Fix with final endpoints for models
# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'data': reverse('data-list', request=request, format=format),
#         'provider': reverse('provider-list', request=request, format=format),
#         'signal': reverse('signal-list', request=request, format=format),
#         'user': reverse('user-list', request=request, format=format),
#     })


class APIListView(APIView):
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


class DataView(RetrieveUpdateDestroyAPIView):
    queryset = Data.objects.all()
    serializer_class = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DataSingleView(ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = opi_serializer.DataSerializer
    permission_classes = (permissions.IsAuthenticated,)


class EventView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class EventSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class MessageView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class MessageSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, requset, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class SettingsView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class SettingsSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = opi_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = opi_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser)

    def provider(self, request, *args, **kwargs):
        signal = self.get_object()
        return Response(signal.provider)

    def pre_save(self, obj):
        obj.user = self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = opi_serializer.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# class ProviderView(View):
#     def get(self, request):
#         pass
#
#
# class ProviderSingleView(View):
#     def get(self, request, id):
#         pass
#
#
# class SettingsView(View):
#     def get(self, request):
#         pass
#
#     def patch(self, request):
#         pass
#
#
# class SignalView(View):
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         pass
#
#
# class SignalSingleView(View):
#     def delete(self, request, id):
#         pass
#
#     def get(self, request, id):
#         pass
#
#     def patch(self, request, id):
#         pass
#
#     def put(self, request, id):
#         pass
#
#
# class UserView(View):
#     def get(self, request):
#         pass
#
#
# class UserSingleView(View):
#     def get(self, request, id):
#         pass
