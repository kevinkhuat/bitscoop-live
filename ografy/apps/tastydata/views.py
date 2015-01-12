from rest_framework.views import APIView as BaseAPIView


class APIView(BaseAPIView):
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
