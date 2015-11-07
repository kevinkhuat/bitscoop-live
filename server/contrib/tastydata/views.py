from django.db.models import Q as Django_Q, QuerySet as Django_QuerySet
from mongoengine import Q as Mongo_Q, QuerySet as Mongo_QuerySet
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView as BaseAPIView

from server.contrib.tastydata import parse_query
from server.contrib.tastydata.pagination import BitscoopItemPagination


def parse_extended_query(query_params, queryset):

    if 'clone' in query_params:
        queryset = queryset.clone()

    elif 'clone_into' in query_params:
        queryset = queryset.clone_into(query_params['clone_into'])

    else:
        if 'only' in query_params:
            # TODO: loop through list to make work for multiple fields
            queryset = queryset.only(query_params['only'])

        if 'exclude' in query_params:
            # TODO: loop through list to make work for multiple fields
            queryset = queryset.exclude(query_params['exclude'])

        if 'distinct' in query_params:
            # TODO: loop through list to make work for multiple fields
            queryset = queryset.distinct(query_params['distinct'])

        if 'hint' in query_params:
            queryset = queryset.distinct(query_params['hint'])

        if 'limit' in query_params:
            queryset = queryset.limit(query_params['limit'])

        if 'skip' in query_params:
            queryset = queryset.limit(query_params['skip'])

        if 'max_time_ms' in query_params:
            queryset = queryset.max_time_ms(query_params['max_time_ms'])

        if 'count' in query_params:
            queryset = queryset.count()

        elif 'average' in query_params:
            queryset = queryset.average(query_params['average'])

        elif 'sum' in query_params:
            queryset = queryset.sum(query_params['sum'])

        elif 'first' in query_params:
            queryset = queryset.first()

    return queryset


class ListMixin(object):
    """
    List a QuerySet.
    """
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(request)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)

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
    pagination_class = BitscoopItemPagination

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
        request.query_filter = parse_query(query_params=request.query_params, expression_class=self.Meta.Q)

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

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # self.queryset = parse_extended_query(query_params=request.query_params, queryset=APIView.queryset)

    class Meta:
        Q = Mongo_Q
        QuerySet = Mongo_QuerySet


class MongoAPIListView(MongoAPIView, OPIListView):
    ordering = 'created'

    class Meta:
        Q = MongoAPIView.Meta.Q
        QuerySet = MongoAPIView.Meta.QuerySet
        list = OPIListView.list
