import json
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from ografy.apps.obase.entities import Event


class EventView (View):

    def get(self, request):
        #Todo: event.get
        data = {}
        return HttpResponse(json.dumps(data), mimetype='applications/json')

    def post(self, request):
        return HttpResponse(json.dumps(Event.post(request.POST.data)), mimetype='applications/json')