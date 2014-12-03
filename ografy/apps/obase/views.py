from django.views.generic import View
from django.http import HttpResponse

from ografy.apps.obase import api
from ografy.apps.obase import documents
from ografy.apps.obase import jsonizer


class SignalSingleView(View):

    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return HttpResponse(self.sj.serialize_list(api.Signal.delete(val=val)))

    def get(self, val):
        return HttpResponse(self.sj.serialize(api.Signal.get(val=val)))

    def patch(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class SignalGroupView(View):

    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return HttpResponse(self.sj.serialize_list(api.Signal.delete(val=val)))

    def get(self):
        return HttpResponse(self.sj.serialize_list(api.Signal.get()))

    def patch(self):
        pass

    def post(self):
        pass


class ProviderSingleView(View):

    def __init__(self):
        super().__init__()
        self.pj = jsonizer.DjangoJsonizer()

    def delete(self):
        raise NotImplementedError

    def get(self, val):
        return HttpResponse(self.pj.serialize(api.Provider.get(val=val)))

    def patch(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class ProviderGroupView(View):

    def __init__(self):
        super().__init__()
        self.pj = jsonizer.DjangoJsonizer()

    def delete(self):
        pass

    def get(self):
        return HttpResponse(self.pj.serialize_list(api.Provider.get()))

    def patch(self):
        pass

    def post(self):
        pass


class DataGroupView(View):

    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()

    def delete(self):
        pass

    def get(self):
        return HttpResponse(self.dj.serialize_list(api.Data.get()))

    def patch(self):
        pass

    def post(self, request):

        # TODO: Fix to use rhobust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_data_list = []

        for data_list_item in post_dict['data_list']:
            saved_data_list.append(api.Data.post(self.dj.deserialize(data_list_item)))

        return HttpResponse(self.dj.serialize_list(saved_data_list))


class DataSingleView(View):

    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()

    def delete(self, val):
        return HttpResponse(self.dj.serialize(api.Data.delete(val=val)))

    def get(self, val):
        return HttpResponse(self.dj.serialize(api.Data.get(val=val)))

    def patch(self, val):
        return HttpResponse(self.dj.serialize(api.Data.patch(val=val)))

    def post(self):
        pass

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_data = api.Data.post(self.dj.deserialize(post_dict['data']))

        return HttpResponse(self.dj.serialize(saved_data))



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

    def delete(self):
        pass


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

    def delete(self):
        pass


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
