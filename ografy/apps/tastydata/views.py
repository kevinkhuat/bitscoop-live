from django.db.models import Q as Django_Q
from django.db.models import QuerySet as Django_QuerySet
from mongoengine import Q as Mongo_Q
from mongoengine import QuerySet as Mongo_QuerySet
from rest_framework import permissions
from rest_framework.views import APIView as BaseAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

import ografy.apps.opi.serializers as opi_serializer
from ografy.apps.tastydata import parse_filter
from ografy.apps.tastydata.pagination import OgrafyItemPagination


class ListMixin(object):
    """
    List a QuerySet.
    """
    def list(self, request, *args, **kwargs):
        QuerySet = self.filter_queryset(request)

        page = self.paginate_queryset(QuerySet)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(QuerySet, many=True)
        return Response(serializer.data)


class OPIListView(ListMixin, GenericAPIView):
    """
    Concrete view for listing a QuerySet.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIView(BaseAPIView):
    filter_backends = (OrderingFilter,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = OgrafyItemPagination

    class Meta:
        Q = Django_Q

    @classmethod
    def get_auth_from_request(cls, request):
        # Create a Q object filtering objects for a specific user
        return cls.Meta.Q(user_id=request.user.id)

    # FIXME: Is this insane to get data from the serializer? Probably.
    @property
    def queryset(self):
        return self.serializer.Meta.model.objects.all()

    @property
    def filter_fields(self):
        return self.serializer.Meta.fields

    def serialize(self, inst, **kwargs):
        if not inst:
            return []
        return self.__class__.serializer(inst, **kwargs).data

    def deserialize(self, data, **kwargs):
        return self.__class__.serializer(**kwargs).to_internal_value(data)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # Transform the request query paramter filter into Q objects that can be used
        # by the django or mongoengine orm
        if hasattr(request, 'query_params'):
            request.query_filter = self.Meta.Q()

            if 'filter' in request.query_params:
                query = request.query_params['filter']
                # add filter query
                request.query_filter = request.query_filter & parse_filter(query, expression_class=self.Meta.Q)
            if 'search' in request.query_params:
                query = request.query_params['search']
                # add search query
                # TODO: Add full text search hook for all text in DB
            # else:
            #     request.query_filter = self.Meta.Q()
        else:
            request.query_filter = self.Meta.Q()

        request.auth_filter = self.get_auth_from_request(request)


class DjangoAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class Meta:
        Q = Django_Q
        QuerySet = Django_QuerySet


class DjangoAPIListView(DjangoAPIView, OPIListView):
    ordering = 'id'

    class Meta:
        Q = DjangoAPIView.Meta.Q
        QuerySet = DjangoAPIView.Meta.QuerySet
        list = OPIListView.list


class MongoAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class Meta:
        Q = Mongo_Q
        QuerySet = Mongo_QuerySet


class MongoAPIListView(MongoAPIView, OPIListView):
    ordering = 'created'

    class Meta:
        Q = MongoAPIView.Meta.Q
        QuerySet = MongoAPIView.Meta.QuerySet
        list = OPIListView.list
