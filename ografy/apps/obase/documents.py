
"""
    ografy.apps.obase.documents
    ~~~~~~~~~~~~~~~~~~

    Logic for the obase mongodb models

    :AUTHORS: Liam Broza
"""
import datetime

from django.conf import settings
import mongoengine as mongo

"""
Connect to mongo as a DB connection instance.
"""
mongo.connect(
    settings.MONGODB_DBNAME,
    host=settings.MONGODB_SERVERNAME,
    port=settings.MONGODB_SERVERPORT
)


class Data(mongo.DynamicDocument):
    """the data class for all uncategorizable data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* the list of uncategorizable data fields
    """

    # To be managed by the REST API
    created = mongo.DateTimeField(default=datetime.datetime.now)
    updated = mongo.DateTimeField(default=datetime.datetime.now)

    # To be sourced from signals.js
    data_blob = mongo.SortedListField(mongo.StringField())


class Event(mongo.Document):
    """the base class for all discrete events tracked by the Ografy engine.

    #. *created* the date created
    #. *updated* the date updated
    #. *user_id* the id of the Django user who the event is associated with
    #. *signal_id* the id of the PSA Signal who the data provider is associated with
    #. *provider_id* the id of the Provider who the PSA Signal is associated with
    #. *provider_name* the name of the Provider who the PSA Signal is associated with

    #. *datetime* the date and time of the event
    #. *data* a class with a list of uncategorizable data fields
    #. *location* the location of the event
    """

    # To be managed by the REST API
    created = mongo.DateTimeField(default=datetime.datetime.now)
    updated = mongo.DateTimeField(default=datetime.datetime.now)
    user_id = mongo.IntField(required=True)
    signal_id = mongo.IntField(required=True)
    provider_id = mongo.IntField(required=True)
    provider_name = mongo.StringField(required=True)

    # To be sourced from signals.js
    datetime = mongo.DateTimeField()
    data = mongo.ReferenceField(Data, reverse_delete_rule=mongo.CASCADE)
    location = mongo.PointField()

    database_id = mongo.IntField()

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
    """This data class for all uncategorizable data.

    #. *event* the base class for all discrete events tracked by the Ografy engine

    #. *message_to* who the message is to
    #. *message_from* who the message is from
    #. *message_body* the body of the message
    """

    # To be managed by the REST API
    event = mongo.ReferenceField(Event, reverse_delete_rule=mongo.CASCADE)

    # To be sourced from signals.js
    message_to = mongo.SortedListField(mongo.StringField())
    message_from = mongo.StringField()
    message_body = mongo.StringField(required=True)
