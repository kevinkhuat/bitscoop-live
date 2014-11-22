import pymongo
import string
from django.conf import settings

from ografy.apps.obase.collections.events import Events

MESSAGES_SPEC = {
    'message_id': {
        'type': int,
        'default': -1,
    },
    'message_to': {
        'type': string,
        'default': 'UNKNOWN',
    },
    'message_from': {
        'type': string,
        'default': 'UNKNOWN',
    },
    'message_body': {
        'type': string,
        'default': 'UNKNOWN',
    },
    'parent': {
        'type': int,
        'default': -1
    }
}


class Messages(Events):
    DB = pymongo.Connection(settings.MONGODB_SERVERNAME, settings.MONGODB_SERVERPORT)[settings.MONGODB_DBNAME]
    collection = DB['messages']
    SPEC = MESSAGES_SPEC
