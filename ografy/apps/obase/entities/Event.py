import pymongo
from ografy.apps.obase.entities import Resource

Events = pymongo.Connection("localhost", 27017)["ografy"]["events"]


class Event(Resource):

    def get(self, username):
        spec = {
            "_id": username,
            "_meta.active": True
        }
        doc = Events.find_one(spec)
        if not doc:
            None

    def put(self, data, username):
        spec = {
            "_id": username,
            "_meta.active": True
        }
        operation = {
            "$set": data.json,
        }
        doc = Events.update(spec, operation, new=True)
        if not doc:
            None

    def _get_message(self, data):
        pass

    def _put_message(self, data):
        pass
