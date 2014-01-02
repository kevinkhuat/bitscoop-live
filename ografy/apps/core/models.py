import uuid

from django.db import models


class User(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=256)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

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
        remote_id: The ID of the account in the remote system. Used as a reference for API methods.
        password: (Encrypted) The password credential used for accessing the connected Account.
        api_key: The API key used to authenticate against foreign APIs.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    root_url = models.CharField(max_length=2048)
    # FIXME: Hash username/passwords with salts. Or cache OAuth credentials (preferred).
    username = models.CharField(max_length=50)
    remote_id = models.IntegerField()
    password = models.CharField(max_length=256)
    api_key = models.CharField(max_length=256)
    
    def __unicode__(self):
        return u'<ACCOUNT_{0}: {1}@{2}>'.format(self.id, self.user.display_name, self.name)


class Metric(models.Model):
    """
    Entity representing a sampled statistic from an Account data-source.
    """
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account)
    url = models.TextField(max_length=2048)
    update_date = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<METRIC: {0}>'.format('TODO')


class Entry(models.Model):
    """
    Entity representing a event-based retrieval from an Account data-source.
    
    Attributes:
        id: A unique database descriptor obtained when saving an Entry.
        account: (Optional) The Account entity to which this event is tied.
        datetime: The date/time the event happened.
        datetime_format: The precision of datetime attribute stored as a format string.
        core: The raw, unparsed core associated with the entry.
        vid: The version identifier of the saved entry.
    """
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    data = models.TextField()
    vid = models.CharField(max_length=32)
    update_date = models.DateTimeField(auto_now=True, db_index=True)

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
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.vid = unicode(uuid.uuid4().hex)
        super(Entry, self).save(force_insert, force_update, *args, **kwargs)
    
    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<ENTRY: {0}>'.format('TODO')
        
        
class Event(Entry):
    """
    Entity representing an occurrence. Abstracted from Entry provided that the retrieved core can be categorized as an Event.
    
    Attributes:
        location: The location of the event stored as a parsable string. (i.e. Latitude/longitude, IP address, or street address)
        location_format: The regex parser to extract core from the location field into a container Location object.
    
    TODO:
        Consider creating an indexible Location object in the database with the most rudimentary locators of latitude/longitude with a FK relation to Events.
    """
    location = models.TextField()
    location_format = models.CharField(max_length=50)
    
    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<EVENT: {0}>'.format('TODO')
        
        
class Message(Event):
    """
    Entity representing an interaction between two Users. Abstracted from Event.
    
    Attributes:
        destination: The location/entity where the Message entity is directed.
        destination_format: The regex parser to extract core from the destination field into a container Destination object.
        payload: The contents of the message delivered
        payload_format: (TODO) The regex parse string to extract the core from the payload field into a container Payload object.
    
    TODO:
        Consider creating an indexible Destination object in the database with a FK relation to other users/companies/orgs and a FK to Message.
    """
    destination = models.TextField()
    destination_format = models.CharField(max_length=50)
    payload = models.TextField()
    
    def __unicode__(self):
        # TODO: Entity Unicode formatting
        return u'<MESSAGE: {0}>'.format('TODO')