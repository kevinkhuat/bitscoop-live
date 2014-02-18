# import uuid
# import base64

from django.db import models


class SimpleBlob(models.Model):
    data = models.TextField()

    # Base64 Encoding example.
    # Can this be implemented while still maintaining searching? Probably not.
    # We'll want to keep this encoding if non-strings can be stored to the core attribute.
    # Otherwise it's an unnecessary performance hit and inconvenience.
    # http://djangosnippets.org/snippets/1597/
    #
    # @property
    # def core(self):
    #     return base64.decodestring(self._data)
    #
    # @core.setter
    # def _set_data(self, core):
    #     self._data = base64.encodestring(core)
    # id = models.AutoField(primary_key=True)
    # source = models.TextField()
    #
    # _data = models.TextField(db_column='data', blank=True)
    #
    # def set_data(self, data):
    #     self._data = base64.encodestring(data)
    #
    # def get_data(self):
    #     return base64.decodestring(self._data)
    #
    # data = property(get_data, set_data)


class BasicLocation(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    name = models.CharField(max_length=300)
    latitude = models.FloatField()  #TODO: min_value=0.0, max_value=360.0)
    longitude = models.FloatField()  # min_value=0.0, max_value=360.0)


class EntityType(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    name = models.CharField(max_length=300)


class AssociationType(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    name = models.CharField(max_length=300)


class Event(models.Model):
    """
    Entity representing an occurance. Abstracted from Entry provided that the retrieved core can be categorized as an Event.

    Attributes:
        location: The location of the event stored as a parsable string. (i.e. Latitutde/longitude, IP address, or street address)
        location_format: The regex parser to extract core from the location field into a container Location object.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    location = models.ForeignKey(BasicLocation)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    dataBlob = models.ForeignKey(SimpleBlob)

    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<EVENT: {0}>'.format('TODO')


class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    name = models.CharField(max_length=300)
    entityType = EntityType
    lastLocation = models.ForeignKey(BasicLocation)
    dataBlob = SimpleBlob


class EntityList(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    name = models.CharField(max_length=300)
    entities = models.ManyToManyField(Entity)


class Association(models.Model):
    id = models.AutoField(primary_key=True)
    # start = Event
    # end = Event
    nodeA = models.ForeignKey(Entity, related_name='association_nodeA')
    nodeB = models.ForeignKey(Entity, related_name='association_nodeB')
    associationType = AssociationType
    associationValue = models.FloatField()


class Message(Event):
    """
    Entity representing an interaction between Users. Abstracted from Event.

    """
    messageId = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Entity, related_name='message_sender')
    recipient = models.ForeignKey(Entity, related_name='message_recipient')
    recipientList = models.ForeignKey(EntityList)

    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<MESSAGE: {0}>'.format('TODO')


class Merchant(Entity):
    merchantId = models.AutoField(primary_key=True)
    products = models.TextField()
    services = models.TextField()
    location = models.ForeignKey(BasicLocation)


class Transaction(Event):
    transactionId = models.AutoField(primary_key=True)
    amount = models.FloatField() # min_value=0.0)
    merchant = models.ForeignKey(Merchant)

#
# class Like(Event):
#     likeId = models.AutoField(primary_key=True)
#
#
# class Post(Message):
#     id = models.AutoField(primary_key=True)
#     likes = models.ManyToManyField(Event)


class Person(Entity):
    personId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=256)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class User(Person):
    """
    Entity representing a User.

    Attributes:
        first_name: Entity-specified given name.
        last_name: Entity-specified inherited name.
        email: Entity-specified email address.
        username: Entity-specified username.
    """
    # TODO: Make sure `account_id` is pulling from the global DB.
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)

    @property
    def display_name(self):
        if len(self.username) == 0:
            return self.email

        return self.username

    def __unicode__(self):
        return u'<USER_{0}: {1},{2}>'.format(self.account_id, self.first_name, self.last_name)


class Account(models.Model):
    """
    Entity representing an integrated Account.

    Attributes:
        id: A unique database descriptor obtained when saving an Account.
        user: A foreign key relationship to the User entity who owns the Account.
        name: The name of the linked service.
        root_url: A URL locator for the root of the connected Account.
        username: (Encrypted) The username login credential used for accessing the connected Account.
        password: (Encrypted) The password credential used for accessing the connected Account.
    """
    accountId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    accountName = models.CharField(max_length=50)
    root_url = models.CharField(max_length=2048)
    # FIXME: Hash username/passwords with salts.
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)

    def __unicode__(self):
        return u'<ACCOUNT_{0}: {1}@{2}>'.format(self.id, self.user.display_name, self.name)