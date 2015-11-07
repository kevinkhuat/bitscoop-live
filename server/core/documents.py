import datetime

import mongoengine
from django.conf import settings


mongoengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
)


class Settings(mongoengine.Document):
    """
    The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """
    LOCATION_ESTIMATION_METHOD = (
        ('Last', 'Last known location'),
        ('Next', 'Next known location'),
        ('Closest', 'Closest location'),
        ('Between', 'Interpolate between last and next'),
    )

    # To be managed by the REST API
    allow_location_collection = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    last_estimate_all_locations = mongoengine.DateTimeField(default=datetime.datetime.now)
    location_estimation_method = mongoengine.StringField(choices=LOCATION_ESTIMATION_METHOD, default='Between')
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)

    meta = {
        'indexes': [{
            'name': 'settings_index',
            'fields': ['$id', '$user_id'],
            'default_language': 'english',
        }]
    }


# Provider and Signal Association documents

class Endpoint(mongoengine.EmbeddedDocument):
    """
    The class representing a Provider's endpoint, e.g. Steam games played

    Attributes:
    id: A unique database descriptor obtained when saving an Endpoint.
    parameter_descriptions: A dictionary of the parameters that can be used on this endpoint and how they are constructed
    route: The full URL for getting the user's data from this Permission
    """

    additional_path_fields = mongoengine.ListField()
    call_method = mongoengine.StringField()
    header_descriptions = mongoengine.DictField()
    name = mongoengine.StringField()
    parameter_descriptions = mongoengine.DictField()
    return_header_descriptions = mongoengine.DictField()
    route = mongoengine.StringField(required=True)


class EventSource(mongoengine.EmbeddedDocument):
    """
    The class representing a data source from a provider, e.g. Steam achievements
    Each EventSource pulls data from one or more Endpoints
    For example, Steam achievements are obtained on a per-game basis, so to get all of your achievements
    you first need to get the list of games played, then use that to get each game's achievements individually

    Attributes:
    id: A unique database descriptor obtained when saving an Endpoint.
    description: A description of what the data this provides
    enabled_by_default: Whether any Permission constructed from this EventSource should be enabled by default
    endpoints: A list of Endpoints that this EventSource uses to get its information
    mapping: How the data returned from the endpoint maps to BitScoop's data schema
    name: The name of the endpoint, e.g. 'Facebook Posts'
    """

    description = mongoengine.StringField(required=True)
    display_name = mongoengine.StringField(required=True)
    enabled_by_default = mongoengine.BooleanField(default=True)
    endpoints = mongoengine.MapField(mongoengine.EmbeddedDocumentField(document_type=Endpoint))
    initial_mapping = mongoengine.StringField()
    mappings = mongoengine.DictField()
    name = mongoengine.StringField(required=True)


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

    auth_backend = mongoengine.StringField()
    auth_type = mongoengine.IntField(choices=AUTH_TYPES)
    backend_name = mongoengine.StringField()
    client_callable = mongoengine.BooleanField(default=True)
    description = mongoengine.StringField()
    domain = mongoengine.StringField()
    endpoint_wait_time = mongoengine.IntField()
    event_sources = mongoengine.MapField(mongoengine.EmbeddedDocumentField(document_type=EventSource))
    name = mongoengine.StringField()
    provider_number = mongoengine.ObjectIdField(primary_key=True)
    tags = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'indexes': [{
            'name': 'provider_index',
            'fields': ['$id'],
            'default_language': 'english'
        }]
    }

    def __str__(self):
        return '{0} {1}'.format(self.id, self.backend_name)


class Permission(mongoengine.EmbeddedDocument):
    """
    The class representing a user's permissions for a specific Signal's EventSource, e.g. the permission to get user A's Facebook Friends list

    Attributes:
    event_source: A reference to the base EventSource for this Permission
    enabled: Whether or not this endpoint will be checked for new data on future runs
    """

    event_source = mongoengine.EmbeddedDocumentField(document_type=EventSource)
    enabled = mongoengine.BooleanField(default=True)


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
        signal_data: Provider-specific data, e.g. account's user_id (not to be confused with the Signal's user_id) and account's handle
    """
    FREQUENCY = (
        (0, 'Premium On Demand'),
        (1, 'Daily'),
        (2, 'Weekly'),
        (3, 'Manual'),
        (4, 'Once'),
    )

    # TODO: Encrypt tokens or remove from Signal
    access_token = mongoengine.StringField()
    complete = mongoengine.BooleanField(default=False)
    connected = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    enabled = mongoengine.BooleanField(default=False)
    endpoint_data = mongoengine.DictField()
    frequency = mongoengine.IntField(default=1, choices=FREQUENCY)
    last_run = mongoengine.DateTimeField()
    name = mongoengine.StringField()
    oauth_token = mongoengine.StringField()
    oauth_token_secret = mongoengine.StringField()
    permissions = mongoengine.MapField(mongoengine.EmbeddedDocumentField(document_type=Permission))
    provider = mongoengine.ReferenceField(Provider, dbref=False)
    refresh_token = mongoengine.StringField()
    signal_data = mongoengine.DictField()
    updated = mongoengine.DateTimeField()
    usa_id = mongoengine.IntField()
    user_id = mongoengine.IntField()

    meta = {
        'indexes': [{
            'name': 'signal_index',
            'fields': ['$id', '$complete', '$connected', '$enabled', '$provider', '$user_id'],
            'default_language': 'english'
        }]
    }

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider)
