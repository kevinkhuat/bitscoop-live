from django.db.models.query import QuerySet
from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata import related_fields
from ografy.apps.tastydata import serializers as tasty_serializers


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


class DataSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Data
        fields = ('id', 'user', 'created', 'updated', 'data_blob')
        depth = 5


class EventSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    data = related_fields.ReferenceField(view_name='event-detail', lookup_field='data', queryset=Data.objects.all())

    # Django References
    user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    signal = related_fields.DjangoField(view_name='signal-detail', lookup_field='signal_id', queryset=Signal.objects.all())
    provider = related_fields.DjangoField(view_name='provider-detail', lookup_field='provider_', queryset=Provider.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'created', 'updated', 'user', 'signal', 'provider', 'provider_name', 'datetime', 'location', 'data')
        depth = 5


class MessageSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    event = related_fields.ReferenceField(view_name='event-detail', lookup_field='event', queryset=Event.objects.all())

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
    # Django References
    user = django_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user.id', queryset=User.objects.all())
    provider = django_serializers.HyperlinkedRelatedField(view_name='provider-detail', lookup_field='provider', queryset=User.objects.all())

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'complete', 'connected', 'enabled', 'frequency', 'created', 'updated')
        depth = 5


class SettingsSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Settings
        fields = ('id', 'user', 'created', 'updated', 'settings_dict')
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    # Mongo References
    settings = related_fields.MongoField(view_name='settings-detail', depth=5, lookup_field='user_id', queryset=User.objects.all())

    # Django References
    signals = related_fields.DjangoField(view_name='signal-detail', lookup_field='user_id', queryset=Signal.objects.all())

    class Meta:
        model = User
        fields = ('id', 'signals', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified', 'settings')
        depth = 5
