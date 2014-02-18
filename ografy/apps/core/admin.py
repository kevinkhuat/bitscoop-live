from django.contrib import admin
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

admin.site.register(SimpleBlob)
admin.site.register(BasicLocation)
admin.site.register(EntityType)
admin.site.register(AssociationType)
admin.site.register(Event)
admin.site.register(Entity)
admin.site.register(EntityList)
admin.site.register(Association)
admin.site.register(Message)
admin.site.register(Merchant)
admin.site.register(Transaction)
admin.site.register(Person)
admin.site.register(User)
admin.site.register(Account)