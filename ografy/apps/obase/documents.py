import datetime

from django.conf import settings
import mongoengine


mongoengine.connect(
    settings.MONGODB['NAME'],
    host=settings.MONGODB['HOST'],
    port=settings.MONGODB['PORT']
    #ssl_certfile=settings.MONGODB['SSL_CERT_FILE'],
    #ssl_cert_reqs=settings.MONGODB['SSL_CERT_REQS'],
    #ssl_ca_certs=settings.MONGODB['SSL_CA_CERTS']
)


class Data(mongoengine.DynamicDocument):
    """The data class for all uncategorizable data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* the list of uncategorizable data fields
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)
    # FIXME: Make sure this is a timezone aware datetime.now. Suggest using Django's version of now.
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)

    # To be sourced from signals.js
    data_blob = mongoengine.SortedListField(mongoengine.StringField())


class Event(mongoengine.Document):
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

    #. *database_id* the id that Mongo uses to reference the event
    """

    # To be managed by the REST API
    # FIXME: Make sure this is a timezone aware datetime.now. Suggest using Django's version of now.
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)
    signal_id = mongoengine.IntField(required=True)
    provider_id = mongoengine.IntField(required=True)
    provider_name = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)

    # To be sourced from signals.js
    datetime = mongoengine.DateTimeField()
    data = mongoengine.ReferenceField(Data, reverse_delete_rule=mongoengine.CASCADE)
    location = mongoengine.PointField()

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


class Message(mongoengine.Document):
    """This data class for all uncategorizable data.

    #. *event* the base class for all discrete events tracked by the Ografy engine

    #. *message_to* who the message is to
    #. *message_from* who the message is from
    #. *message_body* the body of the message
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)
    event = mongoengine.ReferenceField(Event, reverse_delete_rule=mongoengine.CASCADE)

    # To be sourced from signals.js
    message_to = mongoengine.SortedListField(mongoengine.StringField())
    message_from = mongoengine.StringField()
    message_body = mongoengine.StringField(required=True)
