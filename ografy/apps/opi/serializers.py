from django.db.models.query import QuerySet
from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata.serializers.custom_drf_mongoengine import serializers as mongo_serializers


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
    # user = django_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Data
        fields = ('id', 'user_id', 'created', 'updated', 'data_blob')
        depth = 5


class EventSerializer(mongo_serializers.DocumentSerializer):
    # user = django_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    # data = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field='data', queryset=Data.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'created', 'updated', 'user_id', 'signal_id', 'provider_id', 'provider_name', 'datetime', 'location', 'data')
        depth = 5


class MessageSerializer(mongo_serializers.DocumentSerializer):
    # event = mongo_serializers.HyperlinkedRelatedField(view_name='event-detail', lookup_field='event', queryset=Event.objects.all())

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
    # user = django_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user.id')
    # provider = django_serializers.HyperlinkedRelatedField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'complete', 'connected', 'enabled', 'frequency', 'created', 'updated')
        depth = 5


class SettingsSerializer(mongo_serializers.DocumentSerializer):
    # user = mongo_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Settings
        fields = ('id', 'user_id', 'created', 'updated', 'data_blob')
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    # signals = django_serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', queryset=Signal.objects.all())

    class Meta:
        model = User
        fields = ('id', 'signals', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified')
        depth = 5
