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

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    signals = serializers.HyperlinkedRelatedField(many=True, view_name='signal-detail', queryset=Signal.objects.all())
    # events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail')
    # messages = serializers.HyperlinkedRelatedField(many=True, view_name='message-detail')
    # events_data = serializers.HyperlinkedRelatedField(many=True, view_name='data-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
