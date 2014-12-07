from rest_framework import serializers

from ografy.apps.core.models import Provider, Signal, User


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'backend_name', 'auth_backend', 'tags')


class SignalSerializer(serializers.HyperlinkedModelSerializer):
    queryset = Signal.objects.all()
    user = serializers.Field(source='user.id')
    provider = serializers.HyperlinkedIdentityField(view_name='signal-provider')

    def to_internal_value(self, data):
        pass

    # TODO: Validate? http://www.django-rest-framework.org/api-guide/fields/
    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: Fix? With custom lookup?
    # signals = serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', queryset=Signal.objects.all())
    # events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')
    # messages = serializers.HyperlinkedRelatedField(many=True, view_name='message-detail')
    # events_data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail')

    # TODO: Validate? http://www.django-rest-framework.org/api-guide/fields/
    def to_internal_value(self, data):
        pass

    class Meta:
        model = User
        fields = ('id', 'email', 'handle', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_verified')
