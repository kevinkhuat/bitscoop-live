import motorengine
from motorengine.utils import serialize

from ografy import settings


class DictField(motorengine.BaseField):
    """
    Field responsible for storing json objects.

    Usage:

    .. testcode:: modeling_fields

        name = JsonField(required=True)

    Available arguments (apart from those in `BaseField`): `None`

    .. note ::

        If ujson is available, MotorEngine will try to use it.
        Otherwise it will fallback to the json serializer that comes with python.
    """

    def validate(self, value):
        try:
            serialize(value)
            return True
        except:
            return False

    def to_son(self, value):
        return value

    def from_son(self, value):
        return value


# Connect to the Mongo server using MotorEngine
motorengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
)


class Provider(motorengine.Document):
    """
    The class representing a third-party service's API

    Attributes:
        _id: A unique database descriptor set in the fixture.
        name: The name of the linked service.
        base_route: The base portion of a provider's API, e.g. https://graph.facebook.com
        backend_name: The name of the linked service according to PSA backend library.
        auth_backend: The PSA backend library
        auth_type: The authorization scheme used; 0 is OAuth2, 1 is OAuth1, and 2 is OpenID
        client_callable: Whether or not the client can call the API directly using the user's access token (if not, the server must make the call)
        description: A short description of the service's functionality
        tags: A list of categories that describe the service, used on the Connect page to sort them by general functionality
    """
    __collection__ = 'provider'

    auth_backend = motorengine.StringField()
    auth_type = motorengine.IntField()
    backend_name = motorengine.StringField()
    base_route = motorengine.StringField()
    client_callable = motorengine.BooleanField(default=True)
    description = motorengine.StringField()
    endpoint_wait_time = motorengine.IntField
    name = motorengine.StringField()
    tags = motorengine.ListField(motorengine.StringField())

    def __str__(self):
        return '{0} {1}'.format(self.id, self.backend_name)


class Signal(motorengine.Document):
    """
    The class representing an account of a Provider

    Attributes:
        id: A unique database descriptor obtained when saving a Signal.
        user_id: A foreign key relationship to the User entity who owns the Signal.
        provider: A reference to the Provider from which this Signal was created.
        name: The name of the linked service.
        usa_id: The User Social Auth's unique identifier for this account
        complete: Indicates that the connection to the account has been verified by the user
        connected: Indicates that the connection to the account has been authorized (not necessarily verified by the user)
        enabled: Indicates that the Signal will fetch updates when requested
        frequency: How often the signal will check the provider API for new data (see tuple below for mapping)
        last_run: The last time the signal hit the provider API to check for new data
        created: When the signal was first created
        updated: When the signal's settings were last updated
        access_token: Stores OAuth2 or OpenID access token
        oauth_token: OAuth1 public token
        oauth_secret_token: OAuth1 private token
        extra_data: Provider-specific data, e.g. account's user (not to be confused with the Signal's user) and account's handle
    """
    __collection__ = 'signal'

    # TODO: Encrypt tokens or remove from Signal

    access_token = motorengine.StringField()
    complete = motorengine.BooleanField(default=False)
    connected = motorengine.BooleanField(default=False)
    created = motorengine.DateTimeField(required=True)
    enabled = motorengine.BooleanField(default=False)
    endpoint_data = DictField()
    frequency = motorengine.IntField()
    last_run = motorengine.DateTimeField()
    name = motorengine.StringField()
    oauth_token = motorengine.StringField()
    oauth_token_secret = motorengine.StringField()
    permissions = DictField()
    provider = motorengine.ReferenceField(Provider)
    refresh_token = motorengine.StringField()
    signal_data = DictField()
    updated = motorengine.DateTimeField(required=True)
    usa_id = motorengine.IntField()
    user_id = motorengine.IntField()

    @property
    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider)


class Settings(motorengine.Document):
    """
    The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """

    __collection__ = 'settings'

    LOCATION_ESTIMATION_METHOD = (
        ('Last', 'Last known location'),
        ('Next', 'Next known location'),
        ('Closest', 'Closest location'),
        ('Between', 'Interpolate between last and next'),
    )

    # To be managed by the REST API
    allow_location_collection = motorengine.BooleanField(default=True)
    created = motorengine.DateTimeField(auto_now_on_insert=True)
    last_estimate_all_locations = motorengine.DateTimeField(auto_now_on_insert=True)
    location_estimation_method = motorengine.StringField()
    updated = motorengine.DateTimeField(auto_now_on_insert=True)
    user_id = motorengine.IntField(required=True)
