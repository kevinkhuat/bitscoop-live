import datetime

import bson
import mongoengine
from django.apps import AppConfig
from elasticsearch import Elasticsearch
from mongoengine import signals

from ografy import settings


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
    verbose_name = 'Elasticsearch Config'

    es.indices.put_mapping(
        index='core',
        doc_type='contact',
        body={
            'properties': {
                'api_id': {
                    'type': 'string'
                },
                'created': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'data_dict': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        }
                    }
                },
                'handle': {
                    'type': 'string'
                },
                'name': {
                    'type': 'string'
                },
                'ografy_unique_id': {
                    'type': 'string'
                },
                'signal': {
                    'type': 'string'
                },
                'updated': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'user_id': {
                    'type': 'long'
                }
            }
        }
    )
    es.indices.put_mapping(
        index='core',
        doc_type='content',
        body={
            'properties': {
                'content_type': {
                    'type': 'string'
                },
                'created': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'data_dict': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        }
                    }
                },
                'file_extension': {
                    'type': 'string'
                },
                'ografy_unique_id': {
                    'type': 'string'
                },
                'owner': {
                    'type': 'string'
                },
                'signal': {
                    'type': 'string'
                },
                'text': {
                    'type': 'string'
                },
                'title': {
                    'type': 'string'
                },
                'updated': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'url': {
                    'type': 'string'
                },
                'user_id': {
                    'type': 'long'
                }
            }
        }
    )
    es.indices.put_mapping(
        index='core',
        doc_type='event',
        body={
            'properties': {
                'contact_interaction_type': {
                    'type': 'string'
                },
                'contacts_list': {
                    'properties': {
                        'api_id': {
                            'type': 'string'
                        },
                        'contact': {
                            'type': 'string'
                        },
                        'created': {
                            'type': 'date',
                            'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                        },
                        'handle': {
                            'type': 'string'
                        },
                        'name': {
                            'type': 'string'
                        },
                        'updated': {
                            'type': 'date',
                            'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                        }
                    }
                },
                'content_list': {
                    'properties': {
                        'content': {
                            'type': 'string'
                        },
                        'content_type': {
                            'type': 'string'
                        },
                        'created': {
                            'type': 'date',
                            'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                        },
                        'file_extension': {
                            'type': 'string'
                        },
                        'owner': {
                            'type': 'string'
                        },
                        'text': {
                            'type': 'string'
                        },
                        'title': {
                            'type': 'string'
                        },
                        'updated': {
                            'type': 'date',
                            'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                        },
                        'url': {
                            'type': 'string'
                        }
                    }
                },
                'created': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'data_dict': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        }
                    }
                },
                'datetime': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'event_type': {
                    'type': 'string'
                },
                'id': {
                    'type': 'string'
                },
                'location': {
                    'type': 'object',
                    'properties': {
                        'estimated': {
                            'type': 'boolean'
                        },
                        'estimation_method': {
                            'type': 'string'
                        },
                        'geo_format': {
                            'type': 'string'
                        },
                        'geolocation': {
                            'type': 'geo_point'
                        },
                        'location': {
                            'type': 'string'
                        },
                        'resolution': {
                            'type': 'float'
                        }
                    }
                },
                'ografy_unique_id': {
                    'type': 'string'
                },
                'provider': {
                    'type': 'string'
                },
                'provider_name': {
                    'type': 'string'
                },
                'signal': {
                    'type': 'string'
                },
                'updated': {
                    'type': 'string',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'user_id': {
                    'type': 'long'
                }
            }
        }
    )
    es.indices.put_mapping(
        index='core',
        doc_type='location',
        body={
            'properties': {
                'data_dict': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        }
                    }
                },
                'datetime': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                },
                'geo_format': {
                    'type': 'string'
                },
                'geolocation': {
                    'type': 'geo_point'
                },
                'resolution': {
                    'type': 'float'
                },
                'signal': {
                    'type': 'string'
                },
                'source': {
                    'type': 'string'
                }
            }
        }
    )


def elasticsearch_transform(document):
    """
    A function that gets all of the information needed to index a document in Elasticsearch and formats it appropriately
    #. *event_id* the id of the base event
    #. *subtype* the event subtype, if there is one
    #. *subtype_include_fields* a list of the subtype-specific fields that should be mapped for Elasticsearch
    """

    return_dict = {}

    if isinstance(document, mongoengine.Document):
        transform_dict = document.to_mongo().to_dict()
    else:
        transform_dict = document

    # Map all of the Event's fields
    for key, value in transform_dict.items():
        # If the field is a reference, get the string of the ID that the reference points to
        # e.g. Permission is a reference, and you would just store that Permission's ID
        if type(value) is mongoengine.Document:
            return_dict[key] = str(value.id)
        # Elasticsearch cannot store ObjectID's, so convert any ID's to just the string of the ID
        elif type(value) is bson.objectid.ObjectId:
            return_dict[key] = str(value)
        # Convert datetimes to ECMA 262 notation, which is yyyy-mm-ddTHH:MM:SS.sssZ
        elif type(value) is datetime.datetime:
            return_dict[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Coordinates are stored in Mongo in GeoJSON format, which is a dictionary containing key-value pairs
        # 'Type': 'Point' and 'coordinates': [lon, lat]
        # Elasticsearch can only store the array of coordinates, so pull just the lat and lon out
        elif key is 'geolocation' or type(value) is 'PointField':
            if value['type'] is 'Point':
                return_dict['geolocation'] = value['coordinates']
        elif type(value) is list:
            return_dict[key] = []
            for list_item in value:
                return_dict[key].append(elasticsearch_transform(list_item))
        elif key is 'location':
            return_dict[key] = elasticsearch_transform(value)
        elif type(value) is str:
            # Reformat dates if they are obtained in string format
            try:
                temp_time = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                return_dict[key] = temp_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            except ValueError:
                return_dict[key] = value
        # In all other cases, return whatever value is stored in Mongo exactly as it is
        else:
            return_dict[key] = value

    return return_dict


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
    allow_location_collection = mongoengine.BooleanField(default=True)
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
    name = mongoengine.StringField()
    parameter_descriptions = mongoengine.DictField()
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
    mapping: How the data returned from the endpoint maps to Ografy's data schema
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
    scheme = mongoengine.StringField()
    tags = mongoengine.StringField()
    url_name = mongoengine.StringField()

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


# Shared documents

class Contact(mongoengine.Document):
    api_id = mongoengine.StringField()
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    data_dict = mongoengine.DictField()
    handle = mongoengine.StringField()
    name = mongoengine.StringField()
    ografy_unique_id = mongoengine.StringField()
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField()

    meta = {
        'indexes': [{
            'name': 'contact_index',
            'fields': ['$id', '$ografy_unique_id', '$user_id'],
            'default_language': 'english',
        }]
    }

    def elasticsearch_transform(self):
        """
        A function that gets all of the information needed to index a contact in Elasticsearch and formats it appropriately
        #. *contact* The contact to be transformed
        """

        return_dict = {}

        # Map all of the Contact's fields
        for index in self:
            # If the field is a reference, get the string of the ID that the reference points to
            # e.g. Permission is a reference, and you would just store that Permission's ID
            if hasattr(self[index], 'id'):
                return_dict[index] = str(self[index]['id'])
            # Coordinates are stored in Mongo in GeoJSON format, which is a dictionary containing key-value pairs
            # 'Type': 'Point' and 'coordinates': [lon, lat]
            # Elasticsearch can only store the array of coordinates, so pull just the lat and lon out
            elif index == 'geolocation':
                return_dict[index] = {}
                if 'coordinates' in self[index].keys():
                    for key in self[index]:
                        return_dict[index][key] = self[index][key]
                    return_dict[index] = self[index]['coordinates']
            # Elasticsearch cannot store ObjectID's, so convert any ID's to just the string of the ID
            elif index == 'id':
                return_dict[index] = str(self[index])
            # Convert datetimes to ECMA 262 notation, which is yyyy-mm-ddTHH:MM:SS.sssZ
            elif type(self[index]) is datetime.datetime:
                return_dict[index] = self[index].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            # In all other cases, return whatever value is stored in Mongo exactly as it is
            else:
                return_dict[index] = self[index]

        return return_dict

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        body = elasticsearch_transform(
            document=document
        )

        # Post the contact to ES
        es.index(
            index='core',
            id=document.id,
            doc_type='contact',
            body=body
        )

signals.post_save.connect(Contact.post_save, sender=Contact)


class Content(mongoengine.Document):
    CONTENT_TYPE = (
        ('photo', 'Photograph'),
        ('video', 'Video'),
        ('game', 'Videogame'),
        ('audio', 'Music, podcast, etc.'),
        ('text', 'Plain text'),
        ('code', 'Computer code'),
        ('file', 'A computer file'),
        ('web_page', 'A web page')
    )

    content_type = mongoengine.StringField(choices=CONTENT_TYPE)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    data_dict = mongoengine.DictField()
    file_extension = mongoengine.StringField()
    ografy_unique_id = mongoengine.StringField()
    owner = mongoengine.StringField()
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    text = mongoengine.StringField()
    title = mongoengine.StringField()
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    url = mongoengine.StringField()
    user_id = mongoengine.IntField()

    meta = {
        'indexes': [{
            'name': 'content_index',
            'fields': ['$id', '$ografy_unique_id', '$user_id'],
            'default_language': 'english',
        }]
    }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        body = elasticsearch_transform(
            document=document
        )

        # Post the location to ES
        es.index(
            index='core',
            id=document.id,
            doc_type='content',
            body=body
        )

signals.post_save.connect(Content.post_save, sender=Content)


class Location(mongoengine.Document):
    GEO_FORMAT = (
        ('lat_lng', 'Latitude and longitude'),
        ('geohash', 'Geohash'),
    )

    data_dict = mongoengine.DictField()
    datetime = mongoengine.DateTimeField(default=datetime.datetime.now)
    geo_format = mongoengine.StringField(required=True, choices=GEO_FORMAT)
    geolocation = mongoengine.PointField(required=True)
    resolution = mongoengine.FloatField()
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    user_id = mongoengine.IntField()

    meta = {
        'indexes': [{
            'name': 'location_index',
            'fields': ['$id', '$geolocation', '$geo_format', '$user_id'],
            'default_language': 'english',
        }]
    }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        body = elasticsearch_transform(
            document=document
        )

        # Post the location to ES
        es.index(
            index='core',
            id=document.id,
            doc_type='location',
            body=body
        )

signals.post_save.connect(Location.post_save, sender=Location)


# Event documents

class EmbeddedContact(mongoengine.EmbeddedDocument):
    api_id = mongoengine.StringField()
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    contact = mongoengine.ReferenceField(Contact, dbref=False)
    handle = mongoengine.StringField()
    name = mongoengine.StringField()
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)


class EmbeddedContent(mongoengine.EmbeddedDocument):
    CONTENT_TYPE = (
        ('photo', 'Photograph'),
        ('video', 'Video'),
        ('game', 'Videogame'),
        ('audio', 'Music, podcast, etc.'),
        ('text', 'Plain text'),
        ('code', 'Computer code'),
        ('file', 'A computer file')
    )

    content = mongoengine.ReferenceField(Content, dbref=False)
    content_type = mongoengine.StringField(choices=CONTENT_TYPE)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    file_extension = mongoengine.StringField()
    owner = mongoengine.StringField()
    text = mongoengine.StringField()
    title = mongoengine.StringField()
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    url = mongoengine.StringField()


class EmbeddedLocation(mongoengine.EmbeddedDocument):
    GEO_FORMAT = (
        ('lat_lng', 'Latitude and longitude'),
        ('geohash', 'Geohash'),
    )

    LOCATION_ESTIMATION_METHOD = (
        ('Last', 'Last known location'),
        ('Next', 'Next known location'),
        ('Closest', 'Closest location'),
        ('Between', 'Interpolate between last and next'),
    )

    estimated = mongoengine.BooleanField()
    estimation_method = mongoengine.StringField(choices=LOCATION_ESTIMATION_METHOD)
    geo_format = mongoengine.StringField(choices=GEO_FORMAT)
    geolocation = mongoengine.PointField()
    location = mongoengine.ReferenceField(Location, dbref=False)
    resolution = mongoengine.FloatField()


class Event(mongoengine.Document):
    """
    The base class for all discrete events tracked by the Ografy engine.

    #  *contact_interaction_type* How the user relates to those in the Contacts List
    #  *contacts_list* A list of Contacts associated with the event
    #  *content_list* A list of content objects associated with the event
    #. *created* the date created
    #  *data_dict* The dictionary of raw data used to construct the event, plus extra data that may be used in the future
    #  *event_type* The type of event
    #. *location* The location of the event
    #  *ografy_unique_id* An ID constructed out of the user_id, signal_id, and elements unique to the event
    #. *provider* The Provider related to the event
    #. *provider_name* The name of the Provider
    #. *signal* The id of the Signal related to the event
    #. *updated* the date updated
    #. *user_id* the id of the Django user who the event is associated with

    #. *datetime* the date and time of the event
    """

    EVENT_TYPE = (
        ('event', 'Basic Event'),
        ('message', 'Basic Message'),
        ('play', 'Media Play'),
        ('edit', 'File Edit'),
        ('comment', 'Commentary on something'),
        ('view', 'Viewing something'),
        ('create', 'Create something'),
        ('call', 'Phone call'),
        ('visit', 'Visited somewhere'),
        ('travel', 'Traveled somwhere'),
        ('eat', 'Eat something'),
        ('transaction', 'Purchase or sell something'),
        ('sleep', 'Sleep'),
        ('exercise', 'Exercise')
    )

    PEOPLE_INTERACTION_TYPE = (
        ('to', 'Sent to others'),
        ('from', 'Sent to you'),
        ('with', 'Done with others')
    )

    contact_interaction_type = mongoengine.StringField(choices=PEOPLE_INTERACTION_TYPE)
    contacts_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(EmbeddedContact))
    content_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(EmbeddedContent))
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    data_dict = mongoengine.DictField()
    event_type = mongoengine.StringField(choices=EVENT_TYPE)
    location = mongoengine.EmbeddedDocumentField(EmbeddedLocation)
    ografy_unique_id = mongoengine.StringField()
    provider = mongoengine.ReferenceField(Provider, dbref=False)
    provider_name = mongoengine.StringField(required=True)
    signal = mongoengine.ReferenceField(Signal, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)

    # Had to move this below updated because the 'created' and 'updated' defaults
    # were incorrectly trying to reference this instead of the builtin package datetime
    datetime = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [{
            'name': 'event_index',
            'fields': ['$id', '$ografy_unique_id', '$signal', '$user_id'],
            'default_language': 'english'
        }]
    }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        body = elasticsearch_transform(
            document=document
        )

        es.index(
            index='core',
            id=document.id,
            doc_type='event',
            body=body
        )

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        es.delete(
            index='core',
            id=document.id,
            doc_type='event'
        )


signals.post_save.connect(Event.post_save, sender=Event)
signals.post_delete.connect(Event.post_delete, sender=Event)
