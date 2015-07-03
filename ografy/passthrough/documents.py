import motorengine

from ografy import settings


# Connect to the Mongo server using MotorEngine
motorengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
    # ssl_certfile=settings.MONGODB['SSL_CERT_FILE'],
    # ssl_cert_reqs=settings.MONGODB['SSL_CERT_REQS'],
    # ssl_ca_certs=settings.MONGODB['SSL_CA_CERTS']
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
    __collection__ = "provider"

    auth_backend = motorengine.StringField()
    auth_type = motorengine.IntField()
    backend_name = motorengine.StringField()
    base_route = motorengine.StringField()
    client_callable = motorengine.BooleanField(default=True)
    description = motorengine.StringField()
    name = motorengine.StringField()
    tags = motorengine.StringField()

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
    __collection__ = "signal"

    # TODO: Encrypt tokens or remove from Signal
    access_token = motorengine.StringField()
    complete = motorengine.BooleanField(default=False)
    connected = motorengine.BooleanField(default=False)
    created = motorengine.DateTimeField(required=True)
    enabled = motorengine.BooleanField(default=False)
    # extra_data = motorengine.JsonField()
    frequency = motorengine.IntField()
    last_run = motorengine.DateTimeField()
    name = motorengine.StringField()
    oauth_token = motorengine.StringField()
    oauth_token_secret = motorengine.StringField()
    provider = motorengine.ReferenceField(Provider)
    updated = motorengine.DateTimeField(required=True)
    usa_id = motorengine.IntField()
    user_id = motorengine.IntField()

    @property
    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider)


class EndpointDefinition(motorengine.Document):
    """
    The class representing an endpoint from a provider, e.g. Facebook Friends list

    Attributes:
    _id: A unique database descriptor obtained when saving an Endpoint Definition.
    name: The name of the endpoint
    path: The portions of a provider's API specific to this endpoint, e.g. ISteamUser/GetFriendList/v0001/ for Steam's Friends list
    provider: A reference to the provider that this Endpoint is associated with
    enabled_by_default: Whether any Authorized Endpoint constructed from this Endpoint Definition should be enabled by default
    parameter_description: A dictionary of the parameters that can be used on this endpoint and how they are constructed
    mapping: How the data returned from the endpoint maps to Ografy's data schema
    """
    __collection__ = "endpoint_definition"

    enabled_by_default = motorengine.BooleanField(default=True)
    mapping = motorengine.JsonField()
    name = motorengine.StringField(required=True)
    parameter_description = motorengine.JsonField()
    provider = motorengine.ReferenceField(Provider)
    path = motorengine.StringField(required=True)


class AuthorizedEndpoint(motorengine.Document):
    """
    The class representing a user's endpoint for a specific Signal, e.g. the endpoint to get user A's Facebook Friends list

    Attributes:
    _id: A unique database descriptor obtained when saving an Authorized Endpoint.
    name: The name of the Authorized Endpoint
    route: The full URL for getting the user's data from this Authorized Endpoint
    provider: A reference to the provider that this Authorized Endpoint is associated with
    user_id: The Ografy ID for this user
    signal: A reference to the Signal that this Authorized Endpoint is related to
    endpoint_definition: A reference to the base endpoint definition for this Authorized Endpoint
    enabled: Whether or not this endpoint will be checked for new data on future runs
    """
    __collection__ = "authorized_endpoint"

    enabled = motorengine.BooleanField(default=True)
    endpoint_definition = motorengine.ReferenceField(EndpointDefinition)
    name = motorengine.StringField(required=True)
    provider = motorengine.ReferenceField(Provider)
    route = motorengine.StringField(required=True)
    signal = motorengine.ReferenceField(Signal)
    user_id = motorengine.IntField()
