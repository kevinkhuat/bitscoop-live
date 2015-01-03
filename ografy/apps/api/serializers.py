from rest_framework import serializers as django_serializers

from ografy.apps.core.models import Provider, Signal


class ProviderSerializer(django_serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'name', 'backend_name', 'auth_backend', 'tags')


class SignalSerializer(django_serializers.HyperlinkedModelSerializer):
    user = django_serializers.Field(source='user.id')
    provider = django_serializers.HyperlinkedIdentityField(view_name='signal-provider')

    class Meta:
        model = Signal
        fields = ('id', 'user', 'provider', 'name', 'psa_backend_uid', 'verified', 'complete', 'permissions', 'frequency', 'created', 'updated')
