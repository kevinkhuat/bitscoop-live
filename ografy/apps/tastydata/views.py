from django.db.models import Q as Django_Q
from mongoengine import Q as Mongo_Q
from rest_framework.views import APIView as BaseAPIView

from ografy.apps.tastydata import parse_filter


class APIView(BaseAPIView):

    @classmethod
    def get_expression_class(cls):
            return Django_Q

    @classmethod
    def get_filter_from_request(cls, request):
        # Transform the request query paramter filter into Q objects that can be used
        # by the django or mongoengine orm
        if hasattr(request, 'query_params'):
            if 'filter' in request.query_params:
                query = request.query_params['filter']
                return parse_filter(query, expression_class=cls.get_expression_class())
            else:
                return None
        else:
            return None

    @classmethod
    def get_auth_from_request(cls, request):
        # Create a Q object filtering objects for a specific user
        return cls.get_expression_class()(user_id=request.user.id)

    # FIXME: Is this insane to get data from the serializer? Probably.
    @property
    def queryset(self):
        return self.serializer.Meta.model.objects.all()

    @property
    def filter_fields(self):
        return self.serializer.Meta.fields

    def serialize(self, inst, **kwargs):
        return self.__class__.serializer(inst, **kwargs).data

    def deserialize(self, data, **kwargs):
        return self.__class__.serializer(**kwargs).to_internal_value(data)

    def initial(self, request, *args, **kwargs):
        BaseAPIView.initial(request, *args, **kwargs)
        # add filter query
        request.query_filter = self.get_filter_from_request(request)
        request.auth_filter = self.get_auth_from_request(request)


class MongoAPIView(APIView):

    @classmethod
    def get_expression_class(cls):
            return Mongo_Q
