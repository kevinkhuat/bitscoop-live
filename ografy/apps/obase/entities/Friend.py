import pymongo
from ografy.apps.obase.entities import Resource

Friends = pymongo.Connection("localhost", 27017)["ografy"]["friend"]


class Friend(Resource):

    def get(self, username):
        spec = {
            "_id": username,
            "_meta.active": True
        }
        doc = Friend.find_one(spec)
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
        doc = Friends.update(spec, operation, new=True)
        if not doc:
            None
