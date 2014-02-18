from tastypie.resources import ModelResource
from ografy.apps.core.models import SimpleBlob
from ografy.apps.core.models import BasicLocation
from ografy.apps.core.models import EntityType
from ografy.apps.core.models import AssociationType
from ografy.apps.core.models import Event
from ografy.apps.core.models import Entity
from ografy.apps.core.models import EntityList
from ografy.apps.core.models import Association
from ografy.apps.core.models import Message
from ografy.apps.core.models import Merchant
from ografy.apps.core.models import Transaction
from ografy.apps.core.models import Person
from ografy.apps.core.models import User
from ografy.apps.core.models import Account


class SimpleBlobResource(ModelResource):
    class Meta:
        queryset = SimpleBlob.objects.all()
        resource_name = 'simpleblob'


class BasicLocationResource(ModelResource):
    class Meta:
        queryset = BasicLocation.objects.all()
        resource_name = 'basiclocation'


class EntityTypeResource(ModelResource):
    class Meta:
        queryset = EntityType.objects.all()
        resource_name = 'entitytype'


class AssociationTypeResource(ModelResource):
    class Meta:
        queryset = AssociationType.objects.all()
        resource_name = 'associationtype'


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'


class EntityResource(ModelResource):
    class Meta:
        queryset = Entity.objects.all()
        resource_name = 'entity'


class EntityListResource(ModelResource):
    class Meta:
        queryset = EntityList.objects.all()
        resource_name = 'entitylist'


class AssociationResource(ModelResource):
    class Meta:
        queryset = Association.objects.all()
        resource_name = 'simpleblob'


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        resource_name = 'Message'


class MerchantResource(ModelResource):
    class Meta:
        queryset = Merchant.objects.all()
        resource_name = 'merchant'


class TransactionResource(ModelResource):
    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'


class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'person'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'