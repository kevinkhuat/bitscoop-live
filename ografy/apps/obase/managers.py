from django.conf import settings
import pymongo

from ografy.apps.obase.util import clean_data


connection = pymongo.Connection(
    host=settings.MONGODB_SERVERNAME,
    port=settings.MONGODB_SERVERPORT
)
database = connection[settings.MONGODB_DBNAME]


def bulk_insert(self, array):
    # Test if array is actually an array. If so iterate and run insert on each one.
    # E.g. for obj in array: obj.insert()


class BaseManager(object):
    def __init__(self, document_model):
        # Test document_model to make sure it's not None
        self.document_model = document_model
        self.collection = database[document_model.collection_name]

    def insert(self, obj):
        # Insert already cleaned objects.
        # You'll want to flatten the object into an array of Entities (or relevant subclasses) before running insert.
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


