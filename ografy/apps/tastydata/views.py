from django.db.models import Q as Django_Q
from mongoengine import Q as Mongo_Q
from rest_framework.views import APIView as BaseAPIView

from ografy.apps.tastydata import parse_filter


class APIView(BaseAPIView):
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
        return self.__class__.serializer(inst, **kwargs).data

    def deserialize(self, data, **kwargs):
        return self.__class__.serializer(**kwargs).to_internal_value(data)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # Transform the request query paramter filter into Q objects that can be used
        # by the django or mongoengine orm
        if hasattr(request, 'query_params'):
            request.query_filter = self.Meta.Q()

            if '$filter' in request.query_params:
                query = request.query_params['$filter']
                # add filter query
                request.query_filter = request.query_filter & parse_filter(query, expression_class=self.Meta.Q)
            if '$search' in request.query_params:
                query = request.query_params['$search']
                # add search query
                # TODO: Add full text search hook for all text in DB
            # else:
            #     request.query_filter = self.Meta.Q()
        else:
            request.query_filter = self.Meta.Q()

        request.auth_filter = self.get_auth_from_request(request)


class DjangoAPIView(APIView):
    class Meta:
        Q = Django_Q


class MongoAPIView(APIView):
    class Meta:
        Q = Mongo_Q
