import datetime

import mongoengine
from django.apps import AppConfig
from elasticsearch import Elasticsearch
from mongoengine import Q, signals

from ografy import settings
from ografy.contrib.estoolbox import EVENT_MAPPING, MAPPED_FIELDS


# Implement SSL/CA CERTS
es = Elasticsearch([{
    'host': settings.ELASTICSEARCH['HOST'],
    'port': settings.ELASTICSEARCH['PORT']
}])

mongoengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
    # ssl_certfile=settings.MONGODB['SSL_CERT_FILE'],
    # ssl_cert_reqs=settings.MONGODB['SSL_CERT_REQS'],
    # ssl_ca_certs=settings.MONGODB['SSL_CA_CERTS']
)


class ElasticsearchConfig(AppConfig):
    name = 'ografy.core'
    verbose_name = "ElasticSearch Config"

    def ready(self):
        es.indices.put_mapping(
            index='core',
            doc_type='event',
            body=EVENT_MAPPING
        )


def transform_to_ES_Event(event_id, subtype=None, event_include_fields=None, subtype_include_fields=None):
    """A function that gets all of the information needed to index an event in Elasticsearch and formats it appropriately
    #. *event_id* the id of the base event
    #. *subtype* the event subtype, if there is one
    #. *eventIncludeFields* a list of the Event-specific fields that should be mapped for Elasticsearch
    #. *subtypeIncludeFields* a list of the subtype-specific fields that should be mapped for Elasticsearch
    """

    return_dict = {}

    # Get the base Event from Mongo
    event = Event.objects.get(pk=event_id)

    # Map all of the Event's fields that are in eventIncludeFields
    for index in event:
        if index in event_include_fields:
            # If the field is a reference, get the string of the ID that the reference points to
            # e.g. authorized endpoint is a reference, and you would just store that authorized endpoint's ID
            if hasattr(event[index], 'id'):
                return_dict[index] = str(event[index]['id'])
            # Coordinates are stored in Mongo in GeoJSON format, which is a dictionary containing key-value pairs
            # 'Type': 'Point' and 'coordinates': [lon, lat]
            # Elasticsearch can only store the array of coordinates, so pull just the lat and lon out
            elif index == 'location' and type(event[index]) is dict:
                if 'coordinates' in event[index].keys():
                    return_dict['location'] = event[index]['coordinates']
            # Elasticsearch cannot store ObjectID's, so convert any ID's to just the string of the ID
            elif index == 'id':
                return_dict[index] = str(event[index])
            # Convert datetimes to ECMA 262 notation, which is YYYY-mm-ddTHH:MM:SS.sssZ
            elif type(event[index]) is datetime.datetime:
                return_dict[index] = event[index].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            # In all other cases, return whatever value is stored in Mongo exactly as it is
            else:
                return_dict[index] = event[index]

    # If a subtype is specified, then its fields need to be mapped as well
    if subtype is not None:
        return_dict['subtype'] = {
            subtype: {}
        }
        # Get the subtype class based that corresponds to the input subtype
        subtype_class = Message if subtype == 'message' else Play
        # Get the subtype object from Mongo
        subtype_inst = subtype_class.objects.get(Q(event=event_id))
        # Map all of the subtype's fields that are in the associated IncludeFields list
        for index in subtype_inst:
            if index in subtype_include_fields:
                # If the field is a reference, get the string of the ID that the reference points to
                # e.g. authorized endpoint is a reference, and you would just store that authorized endpoint's ID
                if hasattr(subtype_inst[index], 'id'):
                    return_dict[index] = str(subtype_inst[index]['id'])
                # Coordinates are stored in Mongo in GeoJSON format, which is a dictionary containing key-value pairs
                # 'Type': 'Point' and 'coordinates': [lon, lat]
                # Elasticsearch can only store the array of coordinates, so pull just the lat and lon out
                if index == 'location' and type(subtype_inst[index]) is dict:
                    if 'coordinates' in subtype_inst[index].keys():
                        return_dict['subtype'][subtype]['location'] = subtype_inst[index]['coordinates']
                # Elasticsearch cannot store ObjectID's, so convert any ID's to just the string of the ID
                elif index == 'id':
                    return_dict['subtype'][subtype][index] = str(subtype_inst[index])
                # Convert datetimes to ECMA 262 notation, which is YYYY-mm-ddTHH:MM:SS.sssZ
                elif type(subtype_inst[index]) is datetime.datetime:
                    return_dict['subtype'][subtype][index] = subtype_inst[index].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                # In all other cases, return whatever value is stored in Mongo exactly as it is
                else:
                    return_dict['subtype'][subtype][index] = subtype_inst[index]

    return return_dict


class Settings(mongoengine.Document):
    """The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """

    # To be managed by the REST API
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    settings_dict = mongoengine.DictField()
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$user_id'],
                'default_language': 'english',
            }]
        }


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
    name = mongoengine.StringField()
    scheme = mongoengine.StringField()
    tags = mongoengine.StringField()

    meta = {
        'indexes':
            [{
                'fields': ['$id'],
                'default_language': 'english'
            }]
        }

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
        extra_data: Provider-specific data, e.g. account's user (not to be confused with the Signal's user) and account's handle
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
    created = mongoengine.DateTimeField(required=True)
    enabled = mongoengine.BooleanField(default=False)
    extra_data = mongoengine.DictField()
    frequency = mongoengine.IntField(default=1, choices=FREQUENCY)
    last_run = mongoengine.DateTimeField()
    name = mongoengine.StringField()
    oauth_token = mongoengine.StringField()
    oauth_token_secret = mongoengine.StringField()
    provider = mongoengine.ReferenceField(Provider, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    updated = mongoengine.DateTimeField(required=True)
    usa_id = mongoengine.IntField()
    user_id = mongoengine.IntField()

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$provider', '$user_id'],
                'default_language': 'english'
            }]
        }

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider)


class EndpointDefinition(mongoengine.Document):
    """
    The class representing an endpoint from a provider, e.g. Facebook Friends list

    Attributes:
    id: A unique database descriptor obtained when saving an Endpoint Definition.
    name: The name of the endpoint
    path: The portions of a provider's API specific to this endpoint, e.g. ISteamUser/GetFriendList/v0001/ for Steam's Friends list
    provider: A reference to the provider that this Endpoint is associated with
    enabled_by_default: Whether any Authorized Endpoint constructed from this Endpoint Definition should be enabled by default
    parameter_description: A dictionary of the parameters that can be used on this endpoint and how they are constructed
    mapping: How the data returned from the endpoint maps to Ografy's data schema
    """

    enabled_by_default = mongoengine.BooleanField(default=True)
    mapping = mongoengine.DictField()
    name = mongoengine.StringField(required=True)
    parameter_description = mongoengine.DictField()
    provider = mongoengine.ReferenceField(Provider, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    path = mongoengine.StringField(required=True)

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$provider'],
                'default_language': 'english'
            }]
        }


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

    enabled = mongoengine.BooleanField(default=True)
    endpoint_definition = mongoengine.ReferenceField(EndpointDefinition, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    name = mongoengine.StringField(required=True)
    provider = mongoengine.ReferenceField(Provider, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    route = mongoengine.StringField(required=True)
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    user_id = mongoengine.IntField()

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$endpoint_definition', '$signal', '$user_id'],
                'default_language': 'english'
            }]
        }


class Event(mongoengine.Document):
    """the base class for all discrete events tracked by the Ografy engine.

    #. *created* the date created
    #. *updated* the date updated
    #. *user_id* the id of the Django user who the event is associated with
    #. *signal* the id of the PSA Signal who the data provider is associated with
    #. *provider* the id of the Provider who the PSA Signal is associated with
    #. *provider_name* the name of the Provider who the PSA Signal is associated with

    #. *datetime* the date and time of the event
    #. *data* a class with a list of uncategorizable data fields
    #. *location* the location of the event

    #. *database* the id that Mongo uses to reference the event
    """

    EVENT_TYPE = (
        ('event', 'Basic Event'),
        ('message', 'Basic Message'),
        ('play', 'Media Play')
    )

    authorized_endpoint = mongoengine.ReferenceField(AuthorizedEndpoint, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    event_type = mongoengine.StringField(choices=EVENT_TYPE)
    location = mongoengine.PointField()
    name = mongoengine.StringField()
    provider = mongoengine.ReferenceField(Provider, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    provider_name = mongoengine.StringField(required=True)
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)

    # Had to move this below updated because the 'created' and 'updated' defaults
    # were incorrectly trying to reference this instead of the builtin package datetime
    datetime = mongoengine.DateTimeField()

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$authorized_endpoint', '$signal', '$user_id'],
                'default_language': 'english'
            }]
        }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        # Check if the event has already been indexed in Elasticsearch
        event_indexed = es.exists(
            index='core',
            id=document.id,
            doc_type='event',
        )

        subtype = document.event_type

        # If the event has been indexed, then we're doing a put or patch
        # In that case, we need to call transform_to_ES_Event with the subtype so that
        # it will to a put/patch of the fully hydrated ES Event, including the subtype fields
        if event_indexed:
            body = transform_to_ES_Event(
                event_id=document.id,
                subtype=subtype,
                event_include_fields=MAPPED_FIELDS['event'],
                subtype_include_fields=MAPPED_FIELDS[subtype]
            )

            es.index(
                index='core',
                id=document.id,
                doc_type='event',
                body=body
            )
        # If the event has not been indexed, then we're doing a post,
        # but only if the event doesn't have a subtype (i.e. subtype is 'event'
        else:
            if subtype == 'event':
                # For posting generic events, do not include a subtype, as there is none
                body = transform_to_ES_Event(
                    event_id=document.id,
                    subtype=None,
                    event_include_fields=MAPPED_FIELDS['event'],
                    subtype_include_fields=[]
                )

                es.index(
                    index='core',
                    id=document.id,
                    doc_type='event',
                    body=body
                )
        # If we're posting an event that has a subtype, that posting to ES will be handled
        # on the API call for the subtype

    @classmethod
    def post_delete(self, sender, document, **kwargs):

        es.delete(
            index="core",
            id=document.id,
            doc_type="event"
        )

signals.post_save.connect(Event.post_save, sender=Event)
signals.post_delete.connect(Event.post_delete, sender=Event)


class Data(mongoengine.Document):
    """The data class for all uncategorizable data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* the list of uncategorizable data fields
    """

    # To be managed by the REST API
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    data_blob = mongoengine.DictField()
    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$event', '$user_id'],
                'default_language': 'english'
            }]
        }


class Message(mongoengine.Document):
    """This data class for all types of messages

    #. *event* the base class for all discrete events tracked by the Ografy engine

    #. *message_to* who the message is to
    #. *message_from* who the message is from
    #. *message_body* the body of the message
    """

    MESSAGE_TYPE = (
        ('message', 'Basic Message'),
        ('email', 'Email'),
        ('im', 'Instant message'),
        ('text', 'Text Message'),
    )

    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    message_body = mongoengine.StringField(required=True)
    message_from = mongoengine.StringField()
    message_to = mongoengine.SortedListField(mongoengine.StringField())
    message_type = mongoengine.StringField(choices=MESSAGE_TYPE)
    user_id = mongoengine.IntField()

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$event', '$user_id'],
                'default_language': 'english'
            }]
        }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        # Whether we're posting, patching, or putting, we need the fully hydrated mapping of the base
        # event and the subtype
        body = transform_to_ES_Event(
            event_id=document.event.id,
            subtype="message",
            event_include_fields=MAPPED_FIELDS['event'],
            subtype_include_fields=MAPPED_FIELDS['message']
        )

        # Post, patch, or put the fully hydrated event to ES
        es.index(
            index="core",
            id=document.event.id,
            doc_type="event",
            body=body
        )

signals.post_save.connect(Message.post_save, sender=Message)


class Play(mongoengine.Document):

    PLAY_TYPE = (
        ('play', 'Basic Play'),
        ('song', 'Listen to Song'),
        ('movie', 'Watch Movie'),
        ('tv', 'Watch TV'),
        ('videogame', 'Play Video Game'),
        ('video', 'Watch Video')
    )

    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    media_url = mongoengine.StringField()
    play_type = mongoengine.StringField(choices=PLAY_TYPE)
    title = mongoengine.StringField()
    user_id = mongoengine.IntField()

    meta = {
        'indexes':
            [{
                'fields': ['$id', '$event', '$user_id'],
                'default_language': 'english'
            }]
        }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        # Whether we're posting, patching, or putting, we need the fully hydrated mapping of the base
        # event and the subtype
        body = transform_to_ES_Event(
            event_id=document.event.id,
            subtype="play",
            event_include_fields=MAPPED_FIELDS["event"],
            subtype_include_fields=MAPPED_FIELDS["play"]
        )

        # Post, patch, or put the fully hydrated event to ES
        es.index(
            index="core",
            id=document.event.id,
            doc_type="event",
            body=body
        )

signals.post_save.connect(Play.post_save, sender=Play)
