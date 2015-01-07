from django.db.models import Q as D_Q
from mongoengine import Q as M_Q

from ografy.apps.tastydata import parse_filter
from ografy.apps.tastydata.api import BaseApi


class Parse:
    @classmethod
    def get_expression_class(cls, is_mongo_query=False):
        if is_mongo_query:
            return M_Q
        else:
            return D_Q

    @classmethod
    def get_filter_from_request(cls, request, is_mongo_query=False):
        # Transform the request query paramter filter into Q objects that can be used
        # by the django or mongoengine orm
        if hasattr(request, 'query_params'):
            if 'filter' in request.query_params:
                query = request.query_params['filter']
                return parse_filter(query, expression_class=cls.get_expression_class(is_mongo_query=is_mongo_query))
            else:
                return None
        else:
            return None

    @classmethod
    def filter_user_from_request(cls, request, is_mongo_query=False):
        # Create a Q object filtering objects for a specific user
        return cls.get_expression_class(is_mongo_query)(user_id=request.user.id)

    @classmethod
    def get_user_and_filter_from_request(cls, request, is_mongo_query=False):
        # Create a Q object filtering objects for a specific user
        return cls.filter_user_from_request(request, is_mongo_query=is_mongo_query) & cls.get_filter_from_request(request, is_mongo_query=is_mongo_query)

    @classmethod
    def get_user_and_pk_filter_from_request(cls, request, pk, is_mongo_query=False):
        return cls.filter_user_from_request(request, is_mongo_query=is_mongo_query) & cls.get_expression_class(is_mongo_query)(pk=pk)


class ViewApi(BaseApi):
    @classmethod
    def filter_get(cls, request):
        # Filters by filter in in request to preform get
        return cls.get(val=Parse.get_filter_from_request(request, is_mongo_query=False))

    @classmethod
    def user_get(cls, request):
        # Filters by user and filter in in request to preform get
        return cls.get(val=Parse.get_user_and_filter_from_request(request, is_mongo_query=cls.is_mongo_query))

    @classmethod
    def user_pk_delete(cls, request, pk):
        # Filters by user and pk to preform delete
        return cls.delete(val=Parse.get_user_and_pk_filter_from_request(request, pk, is_mongo_query=True))

    @classmethod
    def user_pk_get(cls, request, pk):
        # Filters by user and pk to preform get
        return cls.get(val=Parse.get_user_and_pk_filter_from_request(request, pk, is_mongo_query=True))
