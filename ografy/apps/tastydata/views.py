from rest_framework.views import APIView as BaseAPIView
from ografy.apps.tastydata.serializers import mongo


class APIView(BaseAPIView):
    serializer = mongo.DocumentSerializer

    # FIXME: Is this insane? Probably.
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
