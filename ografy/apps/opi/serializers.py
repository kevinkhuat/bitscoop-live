from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import (
    AuthorizedEndpoint, Data, EndpointDefinition, Event, Message, Play, Provider, Settings, Signal
)
from ografy.apps.core.models import User
from ografy.apps.tastydata import serializers as tasty_serializers


def evaluate(query, QuerySet, many=True):
    # If the queryset has already been evaluated by the internal API send the result directly to the serializer
    if not isinstance(query, QuerySet):
        return query
    else:
        # evaluating badly formed queries just result in an empty response
        try:
            data = list(query)
        except Exception:
            return []
        # If the result of the query is none, send an empty set to the serializer
        if data is None:
            return []
        else:
            if len(data) is 1 and many is False:
                return data[0]
            return data


class DataSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Data
        fields = (
            'id',
            'created',
            'updated',
            'data_blob'
            # 'user'
        )
        depth = 5


class EventSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # data = related_fields.ReferenceField(lookup_field='data', queryset=Data.objects.all(), view_name='data-detail')

    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    # signal = related_fields.DjangoField(view_name='signal-detail', lookup_field='signal_id', queryset=Signal.objects.all())
    # provider = related_fields.DjangoField(view_name='provider-detail', lookup_field='provider_', queryset=Provider.objects.all())

    class Meta:
        model = Event
        fields = (
            'id',
            'event_type',
            'subtype_id',
            'created',
            'updated',
            'data',
            'user_id',
            'signal_id',
            'provider_id',
            'provider_name',
            'datetime',
            'location',
            'name'
            # 'data'
        )
        depth = 5


class MessageSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Message
        fields = (
            'id',
            'user_id',
            'event',
            'message_type',
            'message_to',
            'message_from',
            'message_body'
            # 'event'
        )
        depth = 5


class PlaySerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Play
        fields = (
            'id',
            'user_id',
            'event',
            'play_type',
            'title',
            # 'event'
        )
        depth = 5


class ProviderSerializer(tasty_serializers.DocumentSerializer):

    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
            'backend_name',
            'base_route',
            'auth_backend',
            'auth_type',
            'client_callable',
            'tags',
            'description'
        )
        depth = 5


class SignalSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='user')
    # provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Signal
        fields = (
            'id',
            'user_id',
            'provider',
            'name',
            'complete',
            'connected',
            'enabled',
            'frequency',
            'created',
            'updated',
            'last_run',
            'extra_data'
        )
        depth = 5


class AuthorizedEndpointSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = AuthorizedEndpoint
        fields = (
            'id',
            'name',
            'route',
            'enabled',
            'user_id',
            'provider',
            'endpoint_definition',
            'signal'
        )
        depth = 5


class EndpointDefinitionSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = EndpointDefinition
        fields = (
            'id',
            'name',
            'route_end',
            'provider',
            'enabled_by_default'
        )
        depth = 5


class SettingsSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Settings
        fields = (
            'id',
            'user',
            'created',
            'updated',
            'settings_dict'
        )
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    # Mongo References
    # settings = related_fields.MongoField(view_name='settings-detail', depth=5, lookup_field='user_id', queryset=User.objects.all())

    # Django References
    # signals = django_serializers.HyperlinkedRelatedField(view_name='signal-list', lookup_field='user_id', queryset=Signal.objects.all())
    # permissions

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'handle',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'is_verified'
            # 'settings'
        )
        depth = 5
