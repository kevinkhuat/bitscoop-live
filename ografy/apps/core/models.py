from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.db import models

from ografy.util.decorators import autoconnect


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50)
    root_url = models.CharField(max_length=2048)
    # FIXME: Hash username/passwords with salts. Or cache OAuth credentials (preferred).
    username = models.CharField(max_length=50)
    #remote_id = models.IntegerField()
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


@autoconnect
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

    def pre_save(self):
        self.vid = uuid.uuid4().hex

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
