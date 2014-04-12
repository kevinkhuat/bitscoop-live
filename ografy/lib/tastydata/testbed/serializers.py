from rest_framework import serializers

from ografy.apps.core import models

from django.core.urlresolvers import reverse


class UserSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name = 'api:user-detail')
    
    class Meta:
        model = models.User
        fields = (
            'account_id',
            'uri',
            'first_name',
            'last_name',
            'email',
            'username'
        )
        
        
class AccountSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name = 'api:account-detail')
    user = serializers.HyperlinkedRelatedField(view_name = 'api:user-detail')
    
    class Meta:
        model = models.Account
        fields = (
            'id',
            'uri',
            'user',
            'name',
            'root_url'
        )
        
        
class EntrySerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name = 'api:entry-detail')
    account = serializers.HyperlinkedRelatedField(view_name = 'api:account-detail')
    data = serializers.Field(source = 'data')
    vid = serializers.Field(source = 'vid')
    update_date = serializers.Field(source = 'update_date')
    
    class Meta:
        model = models.Entry
        fields = (
            'id',
            'uri',
            'account',
            'datetime',
            'datetime_format',
            'data',
            'vid',
            'update_date'
        )
        
        
class EventSerializer(EntrySerializer):
    class Meta:
        model = models.Event
        fields = (
            'id',
            'uri',
            'account',
            'datetime',
            'datetime_format',
            'location',
            'location_format',
            'data',
            'vid',
            'update_date'
        )
        
        
class MessageSerializer(EventSerializer):
    payload = serializers.Field(source = 'payload')
    
    class Meta:
        model = models.Message
        fields = (
            'id',
            'uri',
            'account',
            'datetime',
            'datetime_format',
            'location',
            'location_format',
            'destination',
            'destination_format',
            'payload',
            'data',
            'vid',
            'update_date'
        )