from rest_framework.views import APIView as BaseAPIView


class APIView(BaseAPIView):
    def serialize(self, inst, **kwargs):
        return self.__class__.serializer(inst, **kwargs).data

    def deserialize(self, data, **kwargs):
        return self.__class__.serializer(**kwargs).to_internal_value(data)
