import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ografy.apps.core.managers import UserManager
from ografy.util.decorators import autoconnect


@autoconnect
class User(AbstractBaseUser, PermissionsMixin):
    """
    Entity representing a User.

    Attributes:
        id: Entity identifier.
        password: (Inherited) The salted and hashed password value.
        email: Entity-specified email address.
        handle: Entity-specified username.
        first_name: Entity-specified given name.
        last_name: Entity-specified inherited name.
        last_login: (Inherited) The date of last login.
        password_date: The date of the last password change.
        is_verified: Flag indicating whether or not the account has been verified.
        is_active: Flag indicating whether or not the account is active.
    """
    id = models.AutoField(primary_key=True)
    # FIXME: Make the email case insensitive unique. Defer to a hacky pre_save for now.
    email = models.EmailField(max_length=256, blank=False, unique=True, db_index=True)
    # FIXME: Make the handle case insensitive unique.
    handle = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    password_date = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    @property
    def is_valid(self):
        return self.is_active and self.is_verified

    @property
    def identifier(self):
        return self.handle or self.email

    @staticmethod
    def get_identifier_filter(email=None, handle=None, both=None):
        if both is not None:
            return models.Q(email_iexact=both) | models.Q(handle_iexact=both)
        elif email is not None:
            return models.Q(email_iexact=email)
        elif handle is not None:
            return models.Q(handle_iexact=handle)

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.handle or self.first_name

    def pre_save(self):
        self.email = self.email.lower()
        if not self.handle:
            self.handle = self.email


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
