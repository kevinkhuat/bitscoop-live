from rest_framework import serializers as django_serializers

from server.contrib.tastydata import serializers as tasty_serializers
from server.core.documents import Connection, Endpoint, Permission, Provider, Settings
from server.core.models import User


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


class ProviderSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Provider
        fields = (
            'auth_backend',
            'auth_type',
            'backend_name',
            'client_callable',
            'description',
            'domain',
            'endpoint_wait_time',
            'name',
            'provider_number',
            'tags',
        )
        depth = 5


class ConnectionSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = django_serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='user_id')
    # provider = django_serializers.HyperlinkedIdentityField(view_name='provider-detail', lookup_field='provider')

    class Meta:
        model = Connection
        fields = (
            'id',
            'auth_status',
            'created',
            'enabled',
            'endpoint_data',
            'frequency',
            'last_run',
            'metadata',
            'name',
            'permissions',
            'provider',
            'updated',
            'usa_id',
            'user_id',
        )
        depth = 15


class PermissionSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Permission
        fields = (
            'source',
            'enabled',
        )
        depth = 5


class EndpointSerializer(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Endpoint
        fields = (
            'additional_path_fields',
            'call_method',
            'header_descriptions',
            'name',
            'parameter_descriptions',
            'return_header_descriptions',
            'route',
        )
        depth = 5


class Source(tasty_serializers.DocumentSerializer):
    class Meta:
        model = Endpoint
        fields = (
            'description',
            'name',
            'enabled_by_default',
            'endpoints',
            'mappings',
            'name'
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
    # signals = django_serializers.HyperlinkedRelatedField(view_name='signal-list', lookup_field='user_id', queryset=Connection.objects.all())
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
