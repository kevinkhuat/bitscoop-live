from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers

from ografy.apps.obase.documents import Event, Data, Message
from ografy.apps.obase.api import Signal as SignalApi, Provider as ProviderApi
from ografy.apps.obase.api import Event as EventApi, Data as DataApi, Message as MessageApi


class SignalSingleView(View):

    def get(self, id):
        return HttpResponse(serializers.serialize(SignalApi.get(val=id)))


class SignalGroupView(View):

    def get(self):
        return HttpResponse(serializers.serialize(SignalApi.get()))


class ProviderSingleView(View):

    def get(self, id):
        return HttpResponse(serializers.serialize((ProviderApi.get(val=id))))


class ProviderGroupView(View):

    def get(self):
        return HttpResponse(serializers.serialize(ProviderApi.get()))


class DataGroupView(View):

    def get(self):
        return HttpResponse(DataApi.get().to_json())

    def post(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_data_list = []

        for data_list_item in post_dict['data_list']:

            saved_data_list.append(DataApi.post(Data.from_json(data_list_item)))

        return HttpResponse(saved_data_list.to_json())


class DataSingleView(View):

    def delete(self, id):
        return HttpResponse(DataApi.delete(val=id).to_json())

    def get(self, id):
        return HttpResponse(DataApi.get(val=id).to_json())

    def patch(self, id,):
        return HttpResponse(DataApi.patch(val=id).to_json())

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_data = DataApi.post(Data.from_json(post_dict['data']))

        return HttpResponse(saved_data.to_json())


class EventGroupView(View):

    def get(self):
        return HttpResponse(EventApi.get().to_json())

    def post(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_event_list = []

        for event_list_item in post_dict['event_list']:

            data_dict = event_list_item['data']
            event_dict = event_list_item['event']
            saved_data = DataApi.post(Data.from_json(data_dict))

            # TODO: Test?
            event_dict['data'] = saved_data.id
            saved_event_list.append(EventApi.post(Event.from_json(event_dict)))

        return HttpResponse(saved_event_list.to_json())


class EventSingleView(View):

    def delete(self, id):
        return HttpResponse(EventApi.delete(val=id).to_json())

    def get(self, id):
        return HttpResponse(EventApi.get(val=id).to_json())

    def patch(self, id,):
        return HttpResponse(EventApi.patch(val=id).to_json())

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        saved_data = DataApi.post(Data.from_json(data_dict))

        # TODO: Test?
        event_dict['data'] = saved_data.id
        saved_event = EventApi.post(Event.from_json(event_dict))

        return HttpResponse(saved_event.to_json())


class MessageGroupView(View):

    def get(self):
        return HttpResponse(EventApi.get().to_json())

    def post(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_message_list = []

        for message_list_item in post_dict['message_list']:

            data_dict = message_list_item['data']
            event_dict = message_list_item['event']
            message_dict = message_list_item['message']
            saved_data = DataApi.post(Data.from_json(data_dict))

            # TODO: Test?
            event_dict['data'] = saved_data.id
            saved_event = EventApi.post(Event.from_json(event_dict))

            message_dict['event'] = saved_event.id
            saved_message_list.append(MessageApi.post(Message.from_json(message_dict)))

        return HttpResponse(saved_message_list.to_json())


class MessageSingleView(View):

    def delete(self, id):
        return HttpResponse(EventApi.delete(val=id).to_json())

    def get(self, id):
        return HttpResponse(EventApi.get(val=id).to_json())

    def patch(self, id,):
        return HttpResponse(EventApi.patch(val=id).to_json())

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())

        data_dict = post_dict['data']
        event_dict = post_dict['event']
        message_dict = post_dict['message']
        saved_data = DataApi.post(Data.from_json(data_dict))

        # TODO: Test?
        event_dict['data'] = saved_data.id
        saved_event = EventApi.post(Event.from_json(event_dict))

        message_dict['event'] = saved_event.id
        saved_message = MessageApi.post(Message.from_json(message_dict))

        return HttpResponse(saved_message.to_json())
