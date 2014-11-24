import pymongo
import string
from django.conf import settings

from ografy.apps.obase.collections.entities import Entities

EVENTS_SPEC = {
    'event_id': {
        'type': int,
        'default': -1,
    },
    'user_id': {
        'type': int,
        'default': -1,
    },
    'signal_id': {
        'type': int,
        'default': -1,
    },
    'provider_id': {
        'type': int,
        'default': -1,
    },
    'provider_name': {
        'type': string,
        'default': 'UNKNOWN',
    },
    'geolocation': {
        'type': string,
        'default': 'UNKNOWN',
    }, 
    'parent': {
        'type': int,
        'default': -1
    }
}


class Events(Entities):
    DB = pymongo.Connection(settings.MONGODB_SERVERNAME, settings.MONGODB_SERVERPORT)[settings.MONGODB_DBNAME]
    collection = DB['events']
    SPEC = EVENTS_SPEC
