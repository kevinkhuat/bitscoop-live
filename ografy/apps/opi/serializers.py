from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata.serializers import mongo as mongo_serializers


def evaluate(query):
    data = list(query)
    if data is None:
        return []
    else:
        return data


class DataSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field=Data.user_id)

    def to_internal_value(self, data):
        return Data.from_json(data)

    class Meta:
        model = Data
        fields = ('id', 'created', 'updated', 'data_blob')
        depth = 5


class EventSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field=Data.user_id)
    # data = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field=Event.data)

    def to_internal_value(self, data):
        return Event.from_json(data)

    class Meta:
        model = Event
        fields = ('id', 'created', 'updated', 'user_id', 'signal_id', 'provider_id', 'provider_name', 'datetime', 'location', 'data')
        depth = 5


class MessageSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field=Data.user_id)
    # event = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field=Message.event)

    def to_internal_value(self, data):
        return Message.from_json(data)

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
    user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field=Signal.user.id)
    provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field=Signal.provider.id)

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'verified', 'complete', 'permissions', 'frequency', 'created', 'updated')
        depth = 5


class SettingsSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field=Settings.user_id)

    def to_internal_value(self, data):
        return Event.from_json(data)

    user = django_serializers.Field(source='user.id')
    provider = django_serializers.HyperlinkedIdentityField(view_name='signal-provider')

    class Meta:
        model = Settings
        fields = ('id', 'user', 'provider', 'name')
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    signals = django_serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail')
    # events = django_serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')
    # messages = django_serializers.HyperlinkedRelatedField(many=True, view_name='message-detail')
    # events_data = django_serializers.HyperlinkedRelatedField(many=True, view_name='data-detail')

    class Meta:
        model = User
        fields = ('signals', 'events', 'messages', 'event_data', 'id', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified')
        depth = 5
