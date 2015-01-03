from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import ografy.apps.api.serializers as api_serializer
from ografy.apps.core import models as core_models

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'provider-list': reverse('provider-list', request=request, format=format),
        'signal-list': reverse('signal-list', request=request, format=format)
    })

# @api_view(['GET', 'POST'])
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = core_models.Provider.objects.all()
    serializer_class = api_serializer.ProviderSerializer
    permission_classes = (permissions.IsAuthenticated,)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
class SignalViewSet(viewsets.ModelViewSet):
    queryset = core_models.Signal.objects.all()
    serializer_class = api_serializer.SignalSerializer
    permission_classes = (permissions.IsAuthenticated,)
