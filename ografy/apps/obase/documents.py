import datetime

from django.conf import settings
import mongoengine as mongo


mongo.connect(
    settings.MONGODB_DBNAME,
    host=settings.MONGODB_SERVERNAME,
    port=settings.MONGODB_SERVERPORT
)


class Data(mongo.DynamicDocument):
    created = mongo.DateTimeField(default=datetime.datetime.now)
    updated = mongo.DateTimeField(default=datetime.datetime.now)

    data_blob = mongo.SortedListField(mongo.StringField())


class Event(mongo.Document):
    created = mongo.DateTimeField(default=datetime.datetime.now)
    updated = mongo.DateTimeField(default=datetime.datetime.now)

    user_id = mongo.IntField(required=True)
    signal_id = mongo.IntField(required=True)
    provider_id = mongo.IntField(required=True)
    provider_name = mongo.StringField(required=True)

    datetime = mongo.DateTimeField()
    data = mongo.ReferenceField(Data, reverse_delete_rule=mongo.CASCADE)
    location = mongo.PointField()

    meta = {
        'indexes': [
            'user_id',
            'signal_id',
            'provider_id',
            (
                'provider_id',
                '+provider_name'
            ),
            [
                (
                    "location",
                    "2dsphere"
                ),
                (
                    "datetime",
                    1
                )
            ]
        ]
    }


class Message(mongo.Document):
    event = mongo.ReferenceField(Event, reverse_delete_rule=mongo.CASCADE)

    message_to = mongo.SortedListField(mongo.StringField())
    message_from = mongo.StringField()
    message_body = mongo.StringField(required=True)
