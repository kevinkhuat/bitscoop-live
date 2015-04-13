from rest_framework import serializers as django_serializers

from ografy.apps.core.documents import Settings
from ografy.apps.core.models import Provider, Signal, User
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.tastydata import related_fields
from ografy.apps.tastydata import serializers as tasty_serializers


def evaluate(query, QuerySet):
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
            # If there is only one result, send that result to the serializer
            if len(data) == 1:
                return data[0]
            # otherwise send the list to the serializer
            return data


class DataSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Data
        fields = ('id', 'created', 'updated', 'data_blob') # , 'user'
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
        fields = ('id', 'created', 'updated', 'user_id', 'signal_id', 'provider_id', 'provider_name', 'datetime', 'location', 'type', 'name') #, 'data'
        depth = 5


class MessageSerializer(tasty_serializers.DocumentSerializer):
    # Mongo References
    # event = related_fields.ReferenceField(lookup_field='event', queryset=Event.objects.all(), view_name='event-detail')

    class Meta:
        model = Message
        fields = ('id', 'message_to', 'message_from', 'message_body') # 'event',
        depth = 5


class ProviderSerializer(django_serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'name', 'backend_name', 'auth_backend', 'tags')
        depth = 5


class SignalSerializer(django_serializers.HyperlinkedModelSerializer):
    # Django References
    # user = django_serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='user.id', queryset=User.objects.all())
    # provider = django_serializers.HyperlinkedRelatedField(view_name='provider-detail', lookup_field='provider', queryset=User.objects.all())

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'complete', 'connected', 'enabled', 'frequency', 'created', 'updated')
        depth = 5


class SettingsSerializer(tasty_serializers.DocumentSerializer):
    # Django References
    # user = related_fields.DjangoField(view_name='user-detail', lookup_field='user_id', queryset=User.objects.all())

    class Meta:
        model = Settings
        fields = ('id', 'user', 'created', 'updated', 'settings_dict')
        depth = 5


class UserSerializer(django_serializers.HyperlinkedModelSerializer):
    # Mongo References
    # settings = related_fields.MongoField(view_name='settings-detail', depth=5, lookup_field='user_id', queryset=User.objects.all())

    # Django References
    # signals = related_fields.DjangoField(view_name='signal-detail', lookup_field='user_id', queryset=Signal.objects.all())

    class Meta:
        model = User
        fields = ('id', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified') #, 'settings', 'signals'
        depth = 5
