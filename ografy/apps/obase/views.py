import json
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from ografy.apps.obase.entities.events import Events


class EventView (View):

    def get(self, request):
        #Todo: event.get
        data = {}
        return JsonResponse(json.dumps(data))

    def post(self, request):
        result = Event.post(dict(request.POST))
        objectID = int.from_bytes(result._ObjectId__id, 'big')

        return JsonResponse({'objectID' : objectID})
