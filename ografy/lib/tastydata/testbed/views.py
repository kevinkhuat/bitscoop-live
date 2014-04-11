from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


from ografy.apps.core import models
from ografy.apps.api.generic.blueprints import APIBlueprint
from ografy.apps.api import serializers


class RootIndex(APIView):
    """
    Top-level index of the API indicating the queryable resources.
    
    Method Summary:
        GET -- Return the directory of resource collection URLs.
    """
    def get(self, request, format=None):
        return Response({
            'users': reverse('api:user-list', request=request, format=format),
            'accounts': reverse('api:account-list', request=request, format=format),
            'entries': reverse('api:entry-list', request=request, format=format),
            'events': reverse('api:event-list', request=request, format=format),
            'messages': reverse('api:message-list', request=request, format=format)
        })
    
    
class UserList(APIBlueprint):
    """
    Handles interactions with the User entity collection.
    
    Method Summary:
        GET -- Returns a collection of User entities.
        POST -- Adds a new User entity to the collection.
    """
    model = models.User
    serializer = serializers.UserSerializer
    collection_methods = ['GET', 'POST']
    
    
class UserDetail(APIBlueprint):
    """
    Handles interactions with an individual User entity.
    
    Method Summary:
        GET -- Retrieves an existing User entity.
        PUT -- Replaces an existing User entity.
        DELETE -- Deletes an existing User entity.
    """
    model = models.User
    serializer = serializers.UserSerializer
    singleton_methods = ['GET', 'PUT', 'DELETE']
    
    
class AccountList(APIBlueprint):
    """
    Handles interactions with the Account entity collection.
    
    Method Summary:
        GET -- Returns a collection of Account entities.
        POST -- Adds a new Account entity to the collection.
    """
    model = models.Account
    serializer = serializers.AccountSerializer
    collection_methods = ['GET', 'POST']
    
    
class AccountDetail(APIBlueprint):
    """
    Handles interactions with an individual Account entity.
    
    Method Summary:
        GET -- Retrieves an existing Account entity.
        PUT -- Replaces an existing Account entity.
        DELETE -- Deletes an existing Account entity.
    """
    model = models.Account
    serializer = serializers.AccountSerializer
    singleton_methods = ['GET', 'PUT', 'DELETE']
    
    
class EntryList(APIBlueprint):
    """
    Handles interactions with the Entry entity collection.
    
    Method Summary:
        GET -- Returns a collection of Entry entities.
        POST -- Adds a new Entry entity to the collection.
    """
    model = models.Entry
    serializer = serializers.EntrySerializer
    collection_methods = ['GET', 'POST']
    
    
class EntryDetail(APIBlueprint):
    """
    Handles interactions with an individual Entry entity.
    
    Method Summary:
        GET -- Retrieves an existing Entry entity.
        PUT -- Replaces an existing Entry entity.
        DELETE -- Deletes an existing Entry entity.
    """
    model = models.Entry
    serializer = serializers.EntrySerializer
    singleton_methods = ['GET', 'PUT', 'DELETE']
    
    
class EventList(APIBlueprint):
    """
    Handles interactions with the Event entity collection.
    
    Method Summary:
        GET -- Returns a collection of Event entities.
        POST -- Adds a new Event entity to the collection.
    """
    model = models.Event
    serializer = serializers.EventSerializer
    collection_methods = ['GET', 'POST']
    
    
class EventDetail(APIBlueprint):
    """
    Handles interactions with an individual Event entity.
    
    Method Summary:
        GET -- Retrieves an existing Event entity.
        PUT -- Replaces an existing Event entity.
        DELETE -- Deletes an existing Event entity.
    """
    model = models.Event
    serializer = serializers.EventSerializer
    singleton_methods = ['GET', 'PUT', 'DELETE']
    
    
class MessageList(APIBlueprint):
    """
    Handles interactions with the Message entity collection.
    
    Method Summary:
        GET -- Returns a collection of Message entities.
        POST -- Adds a new Message entity to the collection.
    """
    model = models.Message
    serializer = serializers.MessageSerializer
    collection_methods = ['GET', 'POST']
    
    
class MessageDetail(APIBlueprint):
    """
    Handles interactions with an individual Message entity.
    
    Method Summary:
        GET -- Retrieves an existing Message entity.
        PUT -- Replaces an existing Message entity.
        DELETE -- Deletes an existing Message entity.
    """
    model = models.Message
    serializer = serializers.MessageSerializer
    singleton_methods = ['GET', 'PUT', 'DELETE']