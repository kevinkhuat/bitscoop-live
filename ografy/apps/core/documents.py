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


class Settings(mongo.DynamicDocument):
    """The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """

    # To be managed by the REST API
    created = mongo.DateTimeField(default=datetime.datetime.now)
    updated = mongo.DateTimeField(default=datetime.datetime.now)

    # To be sourced from signals.js
    data_blob = mongo.SortedListField(mongo.StringField())
