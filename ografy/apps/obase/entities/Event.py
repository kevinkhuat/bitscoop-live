import pymongo
from django.conf import settings

Events = pymongo.Connection(settings.MONGODB_SERVERNAME, settings.MONGODB_SERVERPORT)[settings.MONGODB_DBNAME]["events"]


class Event(object):

    def get(query):
        spec = {
            "_meta.active": True
        }
        doc = Events.find_one(spec)
        if not doc:
            None

    def get_all(self):
        return Events.find()

    def post(data):
        #Todo: clean data about to be inserted as an Event
        return Events.insert(data)

    def _get_message(data):
        pass

    def _put_message(data):
        pass
