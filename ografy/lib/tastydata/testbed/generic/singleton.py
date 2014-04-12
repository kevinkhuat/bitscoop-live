from rest_framework import status
from rest_framework.response import Response


def _get_singleton(self, request, pk, format=None):
    resource = self.get_object(pk)
    serializer = self.get_serializer(instance=resource, data=request.DATA)

    return Response(serializer.data)


def _put_singleton(self, request, pk, format=None):
    resource = self.get_object(pk)
    serializer = self.get_serializer(instance=resource, data=request.DATA)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _delete_singleton(self, request, pk, format=None):
    resource = self.get_object(pk)
    resource.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


singleton_methods = {
    'GET': _get_singleton,
    'PUT': _put_singleton,
    'DELETE': _delete_singleton,
}