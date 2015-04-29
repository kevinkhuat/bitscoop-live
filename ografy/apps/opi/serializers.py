from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User, Permission, PermissionTemplate
from ografy.apps.obase.documents import Data, Event, Message, Play
from ografy.apps.tastydata import related_fields
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
        ) # , 'user'
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
            'created',
            'updated',
            'data',
            'user_id',
            'signal_id',
            'provider_id',
            'provider_name',
            'datetime',
            'location',
            'name',
            '_cls'
        ) #, 'data'
        depth = 5


class MessageSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Message
        fields = (
            'id',
            'event',
            'message_to',
            'message_from',
            'message_body'
        ) # 'event',
        depth = 5


class PlaySerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Play
        fields = (
            'id',
            'event',
            'title'
        ) # 'event',
        depth = 5


class ProviderSerializer(django_serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
            'backend_name',
            'auth_backend',
            'tags',
            'permissiontemplate_set'
        )
        depth = 5


class SignalSerializer(django_serializers.HyperlinkedModelSerializer):
    # Django References
    # user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='user')
    # provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Signal
        fields = (
            'id',
            'user',
            'provider',
            'name',
            'psa_backend_uid',
            'complete',
            'connected',
            'enabled',
            'frequency',
            'created',
            'updated',
            'access_token',
            'oauth_token',
            'oauth_token_secret',
            'permission_set'
        )
        depth = 5


class PermissionSerializer(django_serializers.ModelSerializer):
    class Meta:
        model = PermissionTemplate
        fields = (
            'id',
            'name',
            'url',
            'provider',
            'enabled',
            'user',
            'permission_template',
            'signal'
        )
        depth = 5


class PermissionTemplateSerializer(django_serializers.ModelSerializer):
    class Meta:
        model = PermissionTemplate
        fields = (
            'id',
            'name',
            'url',
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
            'is_verified',
            'signal_set',
            'permission_set'
        ) #, 'settings'
        depth = 5
