from rest_framework import serializers as django_serializers

from ografy.contrib.tastydata import serializers as tasty_serializers
from ografy.core.documents import Data, Endpoint, Event, Location, Message, Permission, Play, Provider, Settings, Signal
from ografy.core.models import User


def evaluate(query, queryset_class, many=True):
    # If the queryset has already been evaluated by the internal API send the result directly to the serializer
    if not isinstance(query, queryset_class):
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


class EmbeddedLocationSerializer(tasty_serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Location
        fields = (
            'estimated',
            'estimation_method',
            'geo_format',
            'geolocation',
            'reverse_geolocation',
            'reverse_geo_format',
            'resolution'
        )
        depth = 5


class LocationSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Location
        fields = (
            'datetime',
            'geo_format',
            'geolocation',
            'reverse_geolocation',
            'reverse_geo_format',
            'resolution',
            'source',
        )
        depth = 5


class DataSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Data
        fields = (
            'id',
            'created',
            'data_blob',
            'event',
            'updated',
            'user_id',
        )
        depth = 5


class EventSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # data = related_fields.ReferenceField(lookup_field='data', queryset=Data.objects.all(), view_name='data-detail')

    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())
    # signal = related_fields.DjangoField(view_name='signal-detail', lookup_field='signal', queryset=Signal.objects.all())
    # provider = related_fields.DjangoField(view_name='provider-detail', lookup_field='provider_', queryset=Provider.objects.all())

    class Meta:
        model = Event
        fields = (
            'id',
            'permission',
            'created',
            'datetime',
            'event_type',
            'location',
            'name',
            'provider',
            'provider_name',
            'signal',
            'updated',
            'user_id',
        )
        depth = 5


class MessageSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Message
        fields = (
            'id',
            'event',
            'message_body',
            'message_from',
            'message_to',
            'message_type',
            'user_id',
        )
        depth = 5


class PlaySerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Play
        fields = (
            'id',
            'event',
            'media_url',
            'play_type',
            'title',
            'user_id',
        )
        depth = 5


class ProviderSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Provider
        fields = (
            'id',
            'auth_backend',
            'auth_type',
            'backend_name',
            'base_route',
            'client_callable',
            'description',
            'name',
            'tags',
        )
        depth = 5


class SignalSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='user_id')
    # provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Signal
        fields = (
            'id',
            'complete',
            'connected',
            'created',
            'enabled',
            'extra_data',
            'frequency',
            'last_run',
            'name',
            'provider',
            'updated',
            'usa_id',
            'user_id',
        )
        depth = 5


class PermissionSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'enabled',
            'endpoint',
            'name',
            'provider',
            'route',
            'signal',
            'user_id',
        )
        depth = 5


class EndpointSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Endpoint
        fields = (
            'id',
            'enabled_by_default',
            'mapping',
            'name',
            'parameter_description',
            'provider',
            'path',
        )
        depth = 5


class SettingsSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Settings
        fields = (
            'id',
            'allow_location_collection',
            'created',
            'last_estimate_all_locations',
            'location_estimation_method',
            'updated',
            'user_id',
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
            'is_active'
            # 'settings'
        )
        depth = 5
