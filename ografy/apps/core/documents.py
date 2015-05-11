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


class Settings(mongoengine.Document):
    """The data class for user settings data.

    #. *created* the date created
    #. *updated* the date updated
    #. *data_blob* a blog of user settings data
    """

    # To be managed by the REST API
    user_id = mongoengine.IntField(required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated = mongoengine.DateTimeField(default=datetime.datetime.now)

    settings_dict = mongoengine.DictField()

    meta = {
        'indexes': [{
            'fields': ['$user_id'],
            'default_language': 'english',
            }]}
