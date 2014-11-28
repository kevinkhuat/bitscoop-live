from ografy.util.api import BaseApi
import ografy.apps.obase.models as models
import ografy.apps.obase.documents as documents



class Signal(BaseApi):
    model = models.Signal


class Provider(BaseApi):
    model = models.Provider


class Event(BaseApi):
    model = documents.Event

    def post(cls, **data):
        postedEventFields = {
            'user_id': int(data['user_id']),
            'signal_id': int(data['signal-id']),
            'provider_id': int(data['provider-id']),
            'provider_name': data['provider-name'],
            'datetime': data['datetime'],
            'created': data['created'],
            'updated': data['updated'],
            'location': int(data['location']),
        }
        postedEvent = Event(user_id = int(data['user-id']))

        postedEvent.signal_id = int(data['signal-id'])
        postedEvent.provider_id = int(data['provider-id'])
        postedEvent.provider_name = data['provider-name']
        postedEvent.datetime = data['datetime']
        postedEvent.created = data['created']
        postedEvent.updated = data['updated']
        postedEvent.location = int(data['location'])

