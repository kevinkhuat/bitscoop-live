import json
import requests
from urllib.parse import parse_qs
from bson import json_util
from datetime import datetime
from ast import literal_eval

from bson.objectid import ObjectId
from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from mongoengine.queryset import QuerySet
from django.http import HttpResponse

from ografy.apps.obase.documents import Event, Data
from ografy.apps.obase.api import Event as EventApi, Data as DataApi


# @login_required
def test(request):
    return render(request, 'test.html')

class EventGroupView(View):

    def get(self, request):
        eventPostback = EventApi.get()

        serializedEvent = eventPostback.to_json()

        return HttpResponse(serializedEvent)

    def post(self, request):
        result = dict(request.POST._iteritems())

        postedEventFields = {}
        postedEventFields['user_id'] = int(result['user-id'])
        postedEventFields['signal_id'] = int(result['signal-id'])
        postedEventFields['provider_id'] = int(result['provider-id'])
        postedEventFields['datetime'] = datetime.strptime(result['datetime'], "%Y-%m-%dT%H:%M:%S")
        postedEventFields['created'] = datetime.strptime(result['created'], "%Y-%m-%dT%H:%M:%S")
        postedEventFields['updated'] = datetime.strptime(result['updated'], "%Y-%m-%dT%H:%M:%S")
        postedEventFields['provider_name'] = result['provider-name']
        postedEventFields['data'] = result['data']

        postedDataFields = {
            'created': postedEventFields['created'],
            'updated': postedEventFields['updated'],
            'data_blob': [postedEventFields['data']]
        }

        postedData = DataApi.post(**postedDataFields)

        postedEventFields['data'] = postedData

        eventPostback = EventApi.post(**postedEventFields)

        serializedEvent = eventPostback.to_json()

        # unserializedEvent = Event.from_json(serializedEvent)

        return HttpResponse(serializedEvent)



class EventSingleView(View):

    def delete(self, id):
        pass

    def get(self, id):
        pass

    def patch(self, id, request):
        pass

    def put(self, id, request):
        # assuming request.body contains json data which is UTF-8 encoded
        json_str = parse_qs(request.body.decode())
        json_str.pop('id')

        for key in list(json_str.keys()):
            json_str[key] = json_str[key][0]
            if key in ['provider-id', 'signal-id', 'user-id']:
                json_str[key] = int(json_str[key])

        #{\"$oid\": \"54755eff4b7575528efc720d\"} "54755eff4b7575528efc720d"

        ObjectID = json_str['db-id'].replace('"', '')

        updateDocument = Event.objects(id=ObjectID)

        updateData = Data.objects(id=hex(int(ObjectID, 16)-1))
        updateData.update_one(set__data_blob=json_str['data'])
        updateData.get().reload()

        updateDocument.update(set__created=json_str['created'], set__datetime=json_str['datetime'],
                              set__db_id=['db_id'], set__provider_id=json_str['provider-id'],
                              set__provider_name=json_str['provider_name'], set__signal_id=json_str['signal-id'],
                              set__updated=json_str['updated'], set__user_id=json_str['user-id']
                              )
        updateDocument.update()
        updateDocument.get().reload()
        # result = Event.put(objectID, dataDict)

        return JsonResponse(ObjectID, safe=False)