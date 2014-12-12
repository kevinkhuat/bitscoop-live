import jsonpickle
from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata.serializers import mongo as mongo_serializers


class DataSerializer(mongo_serializers.DocumentSerializer):

    def to_internal_value(self, data):
        return Data.from_json(data)

    class Meta:
        model = Data
        fields = ('id', 'created', 'updated', 'data_blob')


class EventSerializer(mongo_serializers.DocumentSerializer):

    def to_internal_value(self, data):
        return Event.from_json(data)

    class Meta:
        model = Event
        fields = ('id', 'created', 'updated', 'user_id', 'signal_id', 'provider_id', 'provider_name', 'datetime',
                  'location', 'data')


class MessageSerializer(mongo_serializers.DocumentSerializer):
    def to_internal_value(self, data):
        return Message.from_json(data)

    class Meta:
        model = Message
        fields = ('id', 'event', 'message_to', 'message_from', 'message_body')


class ProviderSerializer(django_serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'name', 'backend_name', 'auth_backend', 'tags')


class SignalSerializer(django_serializers.HyperlinkedModelSerializer):
    user = django_serializers.Field(source='user.id')
    provider = django_serializers.HyperlinkedIdentityField(view_name='signal-provider')

    class Meta:
        model = Settings
        fields = ('id', 'created', 'updated', 'data_blob')


class SettingsSerializer(mongo_serializers.DocumentSerializer):

    def to_internal_value(self, data):
        return Event.from_json(data)

    user = django_serializers.Field(source='user.id')
    provider = django_serializers.HyperlinkedIdentityField(view_name='signal-provider')

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name')


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    user = django_serializers.Field(source='self')

    # TODO: Fix? With custom lookup?
    # signals = serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', queryset=Signal.objects.all())
    # events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')
    # messages = serializers.HyperlinkedRelatedField(many=True, view_name='message-detail')
    # events_data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail')

    class Meta:
        model = User
        fields = ('id', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified')
