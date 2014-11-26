from rest_framework import status
from rest_framework.response import Response


def _get_collection(self, request, format=None):
    resource = self.get_queryset().all()
    serializer = self.get_serializer(instance=resource, data=request.DATA, many=True)

    return Response(serializer.data)


def _post_collection(self, request, format=None):
    serializer = self.get_serializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

collection_methods = {
    'GET': _get_collection,
    'POST': _post_collection,
}