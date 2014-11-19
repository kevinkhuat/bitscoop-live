import pymongo
from django.conf import settings

Events = pymongo.Connection(settings.MONGODB_SERVERNAME, settings.MONGODB_SERVERPORT)[settings.MONGODB_DBNAME]["events"]


class Event(object):

    def get(self, query):
        spec = {
            "_meta.active": True
        }
        doc = Events.find_one(spec)
        if not doc:
            None

    def post(self, data):
        #Todo: clean data about to be inserted as an Event
        return Events.insert(data)

    def _get_message(self, data):
        pass

    def _put_message(self, data):
        pass
