from django.db.models.query import QuerySet
from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata.rest_framework_mongoengine import serializers as mongo_serializers


# TODO: Move to API, Tastadata View, or View?
def evaluate(query):
    if type(query) is not QuerySet:
        return query
    else:
        data = list(query)
        if data is None:
            return []
        else:
            return data


class DataSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    # def to_internal_value(self, data):
    #     return Data.from_json(data)

    class Meta:
        model = Data
        fields = ('id', 'created', 'updated', 'data_blob')
        depth = 5


class EventSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    # data = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field='data', queryset=Data.objects.all())

    # def to_internal_value(self, data):
    #     return Event.from_json(data)

    class Meta:
        model = Event
        fields = ('id', 'created', 'updated', 'user_id', 'signal_id', 'provider_id', 'provider_name', 'datetime', 'location', 'data')
        depth = 5


class MessageSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    # event = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field='event', queryset=Event.objects.all())

    # def to_internal_value(self, data):
    #     return Message.from_json(data)

    class Meta:
        model = Message
        fields = ('id', 'event', 'message_to', 'message_from', 'message_body')
        depth = 5


class ProviderSerializer(django_serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'name', 'backend_name', 'auth_backend', 'tags')
        depth = 5


class SignalSerializer(django_serializers.HyperlinkedModelSerializer):
    # user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='user.id')
    # provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'verified', 'complete', 'permissions', 'frequency', 'created', 'updated')
        depth = 5


class SettingsSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    # def to_internal_value(self, data):
    #     return Event.from_json(data)

    user = django_serializers.Field(source='user.id')
    provider = django_serializers.HyperlinkedIdentityField(view_name='signal-provider')

    class Meta:
        model = Settings
        fields = ('id', 'user', 'provider', 'name')
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    # signals = django_serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', queryset=Signal.objects.all())
    # events = django_serializers.HyperlinkedRelatedField(many=True, view_name='event-detail', queryset=Events.objects.all())
    # messages = django_serializers.HyperlinkedRelatedField(many=True, view_name='message-detail', queryset=Messages.objects.all())
    # events_data = django_serializers.HyperlinkedRelatedField(many=True, view_name='data-detail', queryset=Data.objects.all())
    # 'signals', 'events', 'messages', 'event_data',

    class Meta:
        model = User
        fields = ('id', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified')
        depth = 5
