from rest_framework import mixins
from rest_framework.viewsets import ViewSetMixin

from ografy.apps.tastydata.serializers.custom_drf_mongoengine.generics import GenericAPIView


class MongoGenericViewSet(ViewSetMixin, GenericAPIView):
    """
    The MongoGenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   MongoGenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           MongoGenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
