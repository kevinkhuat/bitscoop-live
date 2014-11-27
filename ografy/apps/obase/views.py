import json
import requests
from urllib.parse import urlparse, parse_qs
from bson import Binary, Code, json_util

from bson.objectid import ObjectId
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from ografy.apps.obase.documents import Event, Data


# @login_required
def test(request):
    return render(request, 'test.html')

class EventView(View):

    def delete(self):
        pass

    def get(self, request):
        # Todo: event.get
        data = {}
        return JsonResponse(json.dumps(data))

    def post(self, request):
        result = request.POST
        postedEvent = Event()

        postedEvent.user_id = int(result['user-id'])
        postedEvent.signal_id = int(result['signal-id'])
        postedEvent.provider_id = int(result['provider-id'])
        postedEvent.provider_name = result['provider-name']
        postedEvent.datetime = result['datetime']
        postedEvent.created = result['created']
        postedEvent.updated = result['updated']
        # postedEvent.location = int(result['location']

        postedData = Data()
        postedData.data_blob = [result['data']]
        postedData.created = postedEvent.created
        postedData.updated = postedEvent.created
        postedEvent.data = postedData

        postedData.save()
        postedEvent.save()

        eventObjectIdJson = json_util.dumps(postedEvent.id)

        return JsonResponse(eventObjectIdJson, safe=False)

    def put(self, request):
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
