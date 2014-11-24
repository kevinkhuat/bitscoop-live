import datetime
from mongoengine import *
from django.conf import settings

connect(
    settings.MONGODB_DBNAME,
    host=settings.MONGODB_SERVERNAME,
    port=settings.MONGODB_SERVERPORT
)


class Event(Document):
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    event_id = IntField(required=True)
    user_id = IntField(required=True)
    signal_id = IntField(required=True)
    provider_id = IntField(required=True)
    provider_name = StringField(required=True)

    datetime = DateTimeField()
    # data = ReferenceField(Data, reverse_delete_rule=CASCADE)
    location = PointField()

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


class Message(Document):
    event = ReferenceField(Event, reverse_delete_rule=CASCADE)

    message_to = SortedListField(StringField())
    message_from = SortedListField(StringField())
    message_body = StringField(required=True)


class Data(DynamicDocument):
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    data_blob = SortedListField(StringField())
