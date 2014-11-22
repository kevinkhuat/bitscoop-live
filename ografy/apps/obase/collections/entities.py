import pymongo
import datetime
import string
from django.conf import settings

from ografy.apps.obase.collections.utils.util import clean_data

ENTITY_SPEC = {
    'entity_added': {
        'type': datetime,
        'default': datetime.now(),
    },
    'entity_updated': {
        'type': datetime,
        'default': datetime.now(),
    },
    'data': {
        'type': [dict, string],
        'default': {},
    },
    'parent': {
        'type': None,
        'default': None
    }
}


class Entities:
    DB = pymongo.Connection(settings.MONGODB_SERVERNAME, settings.MONGODB_SERVERPORT)[settings.MONGODB_DBNAME]
    collection = DB['entities']
    SPEC = ENTITY_SPEC

    def insert(self, data):
        cleaned_data = clean_data(self.SPEC, data)
        if cleaned_data['parent'] is not None:
            parent = super().insert(data)
            cleaned_data['parent'] = parent
        return self.collection.insert(cleaned_data)

    def find(self, query):
        return self.collection.find(query)

    def update(self, query, data):
        cleaned_data = clean_data(self.SPEC, data)
        if cleaned_data['parent'] is not None:
            parent = super().update({'_id': cleaned_data['parent']}, data)
            cleaned_data['parent'] = parent
        return self.collection.update(query, {"$set": cleaned_data})

    def remove(self, query):
        return self.collection.remove(query)
