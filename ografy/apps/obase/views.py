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
        postedEvent = Event(**request.POST)
        # postedEvent = Event(user_id = int(result['user-id']))
        # postedEvent.signal_id = int(result['signal-id'])
        # postedEvent.provider_id = int(result['provider-id'])
        # postedEvent.provider_name = result['provider-name']
        # postedEvent.datetime = result['datetime']
        # postedEvent.created = result['created']
        # postedEvent.updated = result['updated']
        # # postedEvent.location = int(result['location']

        postedData = Data(**result['data'])
        # postedData.created = postedEvent.created
        # postedData.updated = postedEvent.created
        # postedEvent.data = postedData

        postedData.save()
        postedEvent.save()

        eventObjectIdJson = json_util.dumps(postedEvent.id)

        return JsonResponse(eventObjectIdJson, safe=False)

    def put(self, request):
        # assuming request.body contains json data which is UTF-8 encoded
        json_str = parse_qs(request.body)

        hexObjectID = hex(json_str['id'][0])

        Event.objects(id=hexObjectID).update_one(provider_id=777)
        # result = Event.put(objectID, dataDict)

        return JsonResponse(Event.object(id=hexObjectID))
