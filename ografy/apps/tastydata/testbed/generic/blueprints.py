from types import MethodType

from django.http import Http404
from rest_framework.views import APIView

from ografy.apps.api.generic.collection import collection_methods
from ografy.apps.api.generic.singleton import singleton_methods


class APIBlueprint(APIView):
    model = None
    serializer = None
    singleton_methods = []
    collection_methods = []
    
    def __init__(self, **kwargs):
        for key in self.collection_methods:
            setattr(self, key.lower(), MethodType(collection_methods[key], self, APIBlueprint))
        
        for key in self.singleton_methods:
            setattr(self, key.lower(), MethodType(singleton_methods[key], self, APIBlueprint))
        
        super(APIBlueprint, self).__init__(**kwargs)
        
    def get_object(self, pk):
        """
        Retrieves an object of the view instance collection identified by the specified primary key.
        If no object is found with the specified primary key, a Django Http404 error is raised.
        """
        model = self.model
        try:
            instance = model.objects.get(pk = pk)
            return instance
        except model.DoesNotExist:
            raise Http404
    
    def get_queryset(self):
        """
        Returns the Django QuerySet that should be used to gather all resources in the view instance collection.
        """
        model = self.model
        return model.objects
        
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            #'view': self, TODO: Find out why this is needed (?)
        }
    
    def get_serializer(self, instance = None, data = None, many = False):
        """
        Return the serializer instance that should be used for validating and deserializing input, and for serializing output.
        """
        serializer = self.serializer
        context = self.get_serializer_context()
        return serializer(instance, data = data, many = many, context = context)