from django.views.generic import View
from django.http import HttpResponse

from ografy.apps.obase import api
from ografy.apps.obase import jsonizer


class SignalSingleView(View):

    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return HttpResponse(self.sj.serialize_list(api.Signal.delete(val=val)), content_type="application/json")

    def get(self, val):
        return HttpResponse(self.sj.serialize(api.Signal.get(val=val)), content_type="application/json")

    def patch(self, val, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.patch(val=val, data=post_dict['data'])),
                            content_type="application/json")

    def post(self, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.patch(data=post_dict['data'])),
                            content_type="application/json")

    def put(self, pk, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.put(pk=pk, data=post_dict['data'])),
                            content_type="application/json")


class SignalGroupView(View):

    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return HttpResponse(self.sj.serialize_list(api.Signal.delete(val=val)), content_type="application/json")

    def get(self):
        return HttpResponse(self.sj.serialize_list(api.Signal.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):
        # TODO: Fix to use rhobust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_data_list = []

        for data_list_item in post_dict['data_list']:
            saved_data_list.append(api.Signal.post(self.sj.deserialize(data_list_item)))

        return HttpResponse(self.sj.serialize_list(saved_data_list), content_type="application/json")

    def put(self):
        raise NotImplementedError


class ProviderSingleView(View):

    def __init__(self):
        super().__init__()
        self.pj = jsonizer.DjangoJsonizer()

    def delete(self):
        raise NotImplementedError

    def get(self, val):
        return HttpResponse(self.pj.serialize(api.Provider.get(val=val)), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class ProviderGroupView(View):

    def __init__(self):
        super().__init__()
        self.pj = jsonizer.DjangoJsonizer()

    def delete(self):
        raise NotImplementedError

    def get(self):
        return HttpResponse(self.pj.serialize_list(api.Provider.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError


class DataGroupView(View):

    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()

    def delete(self, val):
        return HttpResponse(self.dj.serialize_list(api.Data.delete(val=val)), content_type="application/json")

    def get(self):
        return HttpResponse(self.dj.serialize_list(api.Data.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):

        # TODO: Fix to use rhobust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_data_list = []

        for data_list_item in post_dict['data_list']:
            saved_data_list.append(api.Data.post(self.dj.deserialize(data_list_item)))

        return HttpResponse(self.dj.serialize_list(saved_data_list), content_type="application/json")

    def put(self):
        raise NotImplementedError


class DataSingleView(View):

    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()

    def delete(self, val):
        return HttpResponse(self.dj.serialize(api.Data.delete(val=val)), content_type="application/json")

    def get(self, val):
        return HttpResponse(self.dj.serialize(api.Data.get(val=val)), content_type="application/json")

    def patch(self, val):
        return HttpResponse(self.dj.serialize(api.Data.patch(val=val)), content_type="application/json")

    def post(self):
        pass

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        saved_data = api.Data.post(self.dj.deserialize(post_dict['data']))

        return HttpResponse(self.dj.serialize(saved_data), content_type="application/json")



class EventGroupView(View):

    def get(self):
        return HttpResponse(EventApi.get().to_json(), content_type="application/json")

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

        return HttpResponse(saved_event_list.to_json()), content_type="application/json"

    def delete(self):
        pass


class EventSingleView(View):

    def delete(self, id):
        return HttpResponse(EventApi.delete(val=id).to_json(), content_type="application/json")

    def get(self, id):
        return HttpResponse(EventApi.get(val=id).to_json(), content_type="application/json")

    def patch(self, id,):
        return HttpResponse(EventApi.patch(val=id).to_json(), content_type="application/json")

    def put(self, request):
        # TODO: Fix?
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        saved_data = DataApi.post(Data.from_json(data_dict))

        # TODO: Test?
        event_dict['data'] = saved_data.id
        saved_event = EventApi.post(Event.from_json(event_dict))

        return HttpResponse(saved_event.to_json(), content_type="application/json")

    def delete(self):
        pass


class MessageGroupView(View):

    def get(self):
        return HttpResponse(EventApi.get().to_json(), content_type="application/json")

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

        return HttpResponse(saved_message_list.to_json(), content_type="application/json")


class MessageSingleView(View):

    def delete(self, id):
        return HttpResponse(EventApi.delete(val=id).to_json(), content_type="application/json")

    def get(self, id):
        return HttpResponse(EventApi.get(val=id).to_json(), content_type="application/json")

    def patch(self, id,):
        return HttpResponse(EventApi.patch(val=id).to_json(), content_type="application/json")

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

        return HttpResponse(saved_message.to_json(), content_type="application/json")
