import json
import requests
import urllib.parse

from bson.objectid import ObjectId
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from ografy.apps.obase.documents import Event


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
        result = Event.post(dict(request.POST))
        objectID = int.from_bytes(result._ObjectId__id, 'big')

        return JsonResponse({'objectID': objectID})

    def put(self, request):
        dataDict = json.loads(request.body.decode('utf-8'))
        dataDict['id'] = ObjectId(int.to_bytes(int(dataDict['id']), 12, 'big'))
        objectID = {'_id': dataDict['id']}

        result = Event.put(objectID, dataDict)

        return JsonResponse({'objectID' : str(dataDict['id'])})

