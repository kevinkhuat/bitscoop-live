import datetime

from django.conf import settings
import mongoengine


mongoengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
    #ssl_certfile=settings.MONGODB['SSL_CERT_FILE'],
    #ssl_cert_reqs=settings.MONGODB['SSL_CERT_REQS'],
    #ssl_ca_certs=settings.MONGODB['SSL_CA_CERTS']
)


class Settings(mongoengine.Document):
    """The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)

    settings_dict = mongoengine.DictField()

    meta = {
        'indexes': [{
            'fields': ['$user_id'],
            'default_language': 'english',
            }]}


class Provider(mongoengine.Document):
    """
    The class representing a third-party service's API

    Attributes:
        id: A unique database descriptor set in the fixture.
        name: The name of the linked service.
        base_route: The base portion of a provider's API, e.g. https://graph.facebook.com
        backend_name: The name of the linked service according to PSA backend library.
        auth_backend: The PSA backend library
        auth_type: The authorization scheme used; 0 is OAuth2, 1 is OAuth1, and 2 is OpenID
        client_callable: Whether or not the client can call the API directly using the user's access token (if not, the server must make the call)
        description: A short description of the service's functionality
        tags: A list of categories that describe the service, used on the Connect page to sort them by general functionality
    """

    AUTH_TYPES = (
        (0, 'OAUTH 2'),
        (1, 'OAUTH 1'),
        (2, 'OPENID')
    )

    name = mongoengine.StringField()

    base_route = mongoengine.StringField()
    backend_name = mongoengine.StringField()
    auth_backend = mongoengine.StringField()
    auth_type = mongoengine.IntField(choices=AUTH_TYPES)

    client_callable = mongoengine.BooleanField(default=True)
    description = mongoengine.StringField()
    tags = mongoengine.StringField()

    def __str__(self):
        return '{0} {1}'.format(self.id, self.backend_name)


class Signal(mongoengine.Document):
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
        extra_data: Provider-specific data, e.g. account's user_id (not to be confused with the Signal's user_id) and account's handle
    """

    FREQUENCY = (
        (0, 'Premium On Demand'),
        (1, 'Daily'),
        (2, 'Weekly'),
        (3, 'Manual'),
        (4, 'Once'),
    )

    user_id = mongoengine.IntField()
    provider = mongoengine.ReferenceField(Provider)
    name = mongoengine.StringField()
    usa_id = mongoengine.IntField()

    complete = mongoengine.BooleanField(default=False)
    connected = mongoengine.BooleanField(default=False)
    enabled = mongoengine.BooleanField(default=False)

    frequency = mongoengine.IntField(default=1, choices=FREQUENCY)
    last_run = mongoengine.DateTimeField()

    created = mongoengine.DateTimeField(required=True)
    updated = mongoengine.DateTimeField(required=True)

    # TODO: Encrypt tokens or remove from Signal
    access_token = mongoengine.StringField()
    oauth_token = mongoengine.StringField()
    oauth_token_secret = mongoengine.StringField()
    extra_data = mongoengine.DictField()

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider, self.user.handle)


class EndpointDefinition(mongoengine.Document):
    """
    The class representing an endpoint from a provider, e.g. Facebook Friends list

    Attributes:
    id: A unique database descriptor obtained when saving an Endpoint Definition.
    name: The name of the endpoint
    route_end: The portions of a provider's API specific to this endpoint, e.g. ISteamUser/GetFriendList/v0001/ for Steam's Friends list
    provider: A reference to the provider that this Endpoint is associated with
    enabled_by_default: Whether any Authorized Endpoint constructed from this Endpoint Definition should be enabled by default
    parameter_description: A dictionary of the parameters that can be used on this endpoint and how they are constructed
    mapping: How the data returned from the endpoint maps to Ografy's data schema
    """

    name = mongoengine.StringField(required=True)
    route_end = mongoengine.StringField(required=True)
    provider = mongoengine.ReferenceField(Provider)
    enabled_by_default = mongoengine.BooleanField(default=True)
    parameter_description = mongoengine.DictField()
    mapping = mongoengine.DictField()


class AuthorizedEndpoint(mongoengine.Document):
    """
    The class representing a user's endpoint for a specific Signal, e.g. the endpoint to get user A's Facebook Friends list

    Attributes:
    id: A unique database descriptor obtained when saving an Authorized Endpoint.
    name: The name of the Authorized Endpoint
    route: The full URL for getting the user's data from this Authorized Endpoint
    provider: A reference to the provider that this Authorized Endpoint is associated with
    user_id: The Ografy ID for this user
    signal: A reference to the Signal that this Authorized Endpoint is related to
    endpoint_definition: A reference to the base endpoint definition for this Authorized Endpoint
    enabled: Whether or not this endpoint will be checked for new data on future runs
    """

    name = mongoengine.StringField(required=True)
    route = mongoengine.StringField(required=True)
    provider = mongoengine.ReferenceField(Provider)
    user_id = mongoengine.IntField()
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE)
    endpoint_definition = mongoengine.ReferenceField(EndpointDefinition)
    enabled = mongoengine.BooleanField(default=True)


class Data(mongoengine.Document):
    """The data class for all uncategorizable data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* the list of uncategorizable data fields
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)

    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)

    event_id = mongoengine.ObjectIdField()

    # To be sourced from signals.js
    data_blob = mongoengine.DictField()


class Event(mongoengine.Document):
    """the base class for all discrete events tracked by the Ografy engine.

    #. *created* the date created
    #. *updated* the date updated
    #. *user_id* the id of the Django user who the event is associated with
    #. *signal_id* the id of the PSA Signal who the data provider is associated with
    #. *provider_id* the id of the Provider who the PSA Signal is associated with
    #. *provider_name* the name of the Provider who the PSA Signal is associated with

    #. *datetime* the date and time of the event
    #. *data* a class with a list of uncategorizable data fields
    #. *location* the location of the event

    #. *database_id* the id that Mongo uses to reference the event
    """

    EVENT_TYPE = (
        ('Event', 'Basic Event'),
        ('Message', 'Basic Message'),
        ('Play', 'Media Play')
    )
    event_type = mongoengine.StringField(choices=EVENT_TYPE)

    subtype_id = mongoengine.ObjectIdField()

    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)
    signal_id = mongoengine.IntField(required=True)
    provider_id = mongoengine.IntField(required=True)
    provider_name = mongoengine.StringField(required=True)
    name = mongoengine.StringField()

    # To be sourced from signals.js
    datetime = mongoengine.DateTimeField()
    data = mongoengine.ReferenceField(Data, reverse_delete_rule=mongoengine.CASCADE)
    location = mongoengine.PointField()

    meta = {
        'indexes': [
            {
                'fields': ['$user_id', '$signal_id', '$name', '$datetime', ("$location","2dsphere")],
                'default_language': 'english',
                'weight': {'name': 10, 'datetime': 2}
            }
        ]
    }


class Message(mongoengine.Document):
    """This data class for all types of messages

    #. *event* the base class for all discrete events tracked by the Ografy engine

    #. *message_to* who the message is to
    #. *message_from* who the message is from
    #. *message_body* the body of the message
    """

    MESSAGE_TYPE = (
        ('Email', 'Email'),
        ('IM', 'Instant message'),
        ('Text', 'Text Message'),
    )

    user_id = mongoengine.IntField()
    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE)
    message_type = mongoengine.StringField(choices=MESSAGE_TYPE)

    # To be sourced from signals.js
    message_to = mongoengine.SortedListField(mongoengine.StringField())
    message_from = mongoengine.StringField()
    message_body = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {
                'fields': ['$message_to', '$message_from', '$message_body'],
                'weight': {'message_body': 10, 'message_to': 2, 'message_from': 2}
            }
        ]
    }


class Play(mongoengine.Document):

    PLAY_TYPE = (
        ('Song', 'Listen to Song'),
        ('Movie', 'Watch Movie'),
        ('TV', 'Watch TV'),
        ('Video Game', 'Play Video Game'),
        ('Video', 'Watch Video')
    )

    user_id = mongoengine.IntField()
    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE)
    play_type = mongoengine.StringField(choices=PLAY_TYPE)

    title = mongoengine.StringField()
    media_url = mongoengine.StringField()

    meta = {
        'indexes': [
            {
                'fields': ['$title'],
                'weight': {'title': 12}
            }
        ]
    }
