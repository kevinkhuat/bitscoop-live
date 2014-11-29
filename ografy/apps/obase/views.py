from urllib.parse import parse_qs
from bson import json_util
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from ografy.apps.obase.documents import Event, Data, Message
from ografy.apps.obase.api import Signal as SignalApi
from ografy.apps.obase.api import Provider as ProviderApi
from ografy.apps.obase.api import Event as EventApi


class SignalSingleView(View):

    def get(self, request, id):
        return HttpResponse(SignalApi.get(val=id))


class SignalGroupView(View):

    def get(self, request):
        return JsonResponse(SignalApi.get())


class ProviderSingleView(View):

    def get(self, request, id):
        return JsonResponse(ProviderApi.get(val=id))


class ProviderGroupView(View):

    def get(self, request):
        return JsonResponse(list(ProviderApi.get()), safe=False)


class EventGroupView(View):

    def get(self):
        return JsonResponse(EventApi.get())

    def post(self, request):

        result = request.POST
        postedEvent = EventApi.post(**result)

        postedData = Data(**result['data'])

        postedData.save()
        postedEvent.save()

        eventObjectIdJson = json_util.dumps(postedEvent.id)

        return JsonResponse(eventObjectIdJson, safe=False)


class EventSingleView(View):

    def delete(self, id):
        JsonResponse(EventApi.delete(val=id))

    def get(self, id):
        JsonResponse(EventApi.get(val=id))

    def patch(self, id, request):
        JsonResponse(EventApi.patch(val=id))

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

        updateDocument.update(set__created=json_str['created'],
                              set__datetime=json_str['datetime'],
                              set__db_id=['db_id'],
                              set__provider_id=json_str['provider-id'],
                              set__provider_name=json_str['provider_name'],
                              set__signal_id=json_str['signal-id'],
                              set__updated=json_str['updated'],
                              set__user_id=json_str['user-id']
                              )
        updateDocument.update()
        updateDocument.get().reload()
        # result = Event.put(objectID, dataDict)

        return JsonResponse(ObjectID, safe=False)
