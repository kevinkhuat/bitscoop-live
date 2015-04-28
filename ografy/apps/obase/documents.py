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


class Data(mongoengine.Document):
    """The data class for all uncategorizable data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* the list of uncategorizable data fields
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)

    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)

    event_id = mongoengine.ObjectIdField()

    # To be sourced from signals.js
    data_blob = mongoengine.DictField()


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

    EVENT_TYPE = (
        ('Event', 'Basic Event'),
        ('Message', 'Basic Message'),
        ('Play', 'Media Play')
    )
    type = mongoengine.StringField(choices=EVENT_TYPE)

    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)
    user_id = mongoengine.IntField(required=True)
    signal_id = mongoengine.IntField(required=True)
    provider_id = mongoengine.IntField(required=True)
    provider_name = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)

    # To be sourced from signals.js
    datetime = mongoengine.DateTimeField()
    location = mongoengine.PointField()

    data = mongoengine.ReferenceField(Data, reverse_delete_rule=mongoengine.CASCADE)

    meta = {
        'indexes': [{
            'fields': ['$user_id', '$signal_id', '$name', '$datetime'],
            'default_language': 'english',
            'weight': {'name': 10, 'datetime': 2}
            }]}


class Message(Event):
    """This data class for all types of messages

    #. *event* the base class for all discrete events tracked by the Ografy engine

    #. *message_to* who the message is to
    #. *message_from* who the message is from
    #. *message_body* the body of the message
    """

    MESSAGE_TYPE = (
        ('Email', 'Email'),
        ('IM', 'Instant message'),
        ('Text', 'Text Message'),
    )

    subtype = mongoengine.StringField(choices=MESSAGE_TYPE)

    # To be sourced from signals.js
    message_to = mongoengine.SortedListField(mongoengine.StringField())
    message_from = mongoengine.StringField()
    message_body = mongoengine.StringField(required=True)

    meta = {
        'indexes': [{
            'fields': ['$message_to', '$message_from', '$message_body'],
            'default_language': 'english',
            'weight': {'message_body': 10, 'message_to': 2, 'message_from': 2}
            }]}


class Play(Event):

    PLAY_TYPE = (
        ('Song', 'Listen to Song'),
        ('Movie', 'Watch Movie'),
        ('TV', 'Watch TV'),
        ('Video Game', 'Play Video Game'),
        ('Video', 'Watch Video')
    )

    subtype = mongoengine.StringField(choices=PLAY_TYPE)

    title = mongoengine.StringField()
    media_url = mongoengine.StringField()

    meta = {
        'indexes': [{
            'fields': ['$title'],
            'default_language': 'english'
            }]}
