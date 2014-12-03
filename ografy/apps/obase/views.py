from django.views.generic import View
from django.http import HttpResponse, JsonResponse

from ografy.apps.obase import api
from ografy.apps.obase import jsonizer


class SignalSingleView(View):
    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return JsonResponse(api.Signal.delete(val=val))

    def get(self, val):
        return HttpResponse(self.sj.serialize(api.Signal.get(val=val)), content_type="application/json")

    def patch(self, val, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.patch(val=val, data=post_dict['signal'])),
                            content_type="application/json")

    def post(self, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.post(data=post_dict['signal'])),
                            content_type="application/json")

    def put(self, pk, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.sj.serialize(api.Signal.put(pk=pk, data=post_dict['signal'])),
                            content_type="application/json")


class SignalGroupView(View):
    def __init__(self):
        super().__init__()
        self.sj = jsonizer.DjangoJsonizer()

    def delete(self, val):
        return JsonResponse(api.Signal.delete(val=val))

    def get(self):
        return HttpResponse(self.sj.serialize_list(api.Signal.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):
        # TODO: Fix to use robust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_list = []

        for list_item in post_dict['signal_list']:
            saved_list.append(api.Signal.post(self.sj.deserialize(list_item)))

        return HttpResponse(self.sj.serialize_list(saved_list), content_type="application/json")

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
        return JsonResponse(api.Data.delete(val=val))

    def get(self):
        return HttpResponse(self.dj.serialize_list(api.Data.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):

        # TODO: Fix to use robust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_list = []

        for list_item in post_dict['data_list']:
            saved_list.append(api.Data.post(self.dj.deserialize(list_item)))

        return HttpResponse(self.dj.serialize_list(saved_list), content_type="application/json")

    def put(self):
        raise NotImplementedError


class DataSingleView(View):
    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()

    def delete(self, val):
        return JsonResponse(api.Data.delete(val=val))

    def get(self, val):
        return HttpResponse(self.dj.serialize(api.Data.get(val=val)), content_type="application/json")

    def patch(self, val, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.dj.serialize(api.Data.patch(val=val, data=post_dict['data'])),
                            content_type="application/json")

    def post(self, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.dj.serialize(api.Data.patch(data=post_dict['data'])),
                            content_type="application/json")

    def put(self, pk, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        return HttpResponse(self.dj.serialize(api.Data.put(pk=pk, data=post_dict['data'])),
                            content_type="application/json")


class EventGroupView(View):
    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()
        self.ej = jsonizer.EventJsonizer()

    def delete(self, val):
        # TODO: Cascade delete to include data collection
        return JsonResponse(api.Event.delete(val=val))

    def get(self):
        return HttpResponse(self.ej.serialize_list(api.Event.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):
        # TODO: Fix to use robust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_list = []

        for list_item in post_dict['event_list']:
            data_dict = list_item['data']
            event_dict = list_item['event']
            # TODO: Make query smarter
            saved_data = api.Data.post(self.dj.deserialize(data_dict))
            event_dict['data'] = saved_data.id
            saved_list.append(api.Event.post(self.ej.deserialize(event_dict)))

        return JsonResponse(saved_list)

    def put(self):
        raise NotImplementedError


class EventSingleView(View):
    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()
        self.ej = jsonizer.EventJsonizer()

    def delete(self, val):
        # TODO: Cascade delete to include data collection
        return JsonResponse(api.Event.delete(val=val))

    def get(self, val):
        return HttpResponse(self.ej.serialize(api.Event.get(val=val)), content_type="application/json")

    def patch(self, val, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        # TODO: Make query smarter
        saved_data = api.Data.patch(val=val, data=self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        saved_event = api.Event.patch(val=val, data=self.ej.deserialize(event_dict))

        return HttpResponse(self.ej.serialize(saved_event), content_type="application/json")

    def post(self, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        # TODO: Make query smarter
        saved_data = api.Data.post(data=self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        saved_event = api.Event.post(data=self.ej.deserialize(event_dict))

        return HttpResponse(self.ej.serialize(saved_event), content_type="application/json")

    def put(self, pk, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        # TODO: Make query smarter
        saved_data = api.Data.put(pk=pk, data=self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        saved_event = api.Event.put(pk=pk, data=self.ej.deserialize(event_dict))

        return HttpResponse(self.ej.serialize(saved_event), content_type="application/json")


class MessageGroupView(View):
    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()
        self.ej = jsonizer.EventJsonizer()
        self.mj = jsonizer.MessageJsonizer()

    def delete(self, val):
        # TODO: Cascade delete to include data and event collections
        return JsonResponse(api.Message.delete(val=val))

    def get(self):
        return HttpResponse(self.mj.serialize_list(api.Message.get()), content_type="application/json")

    def patch(self):
        raise NotImplementedError

    def post(self, request):
        # TODO: Fix to use robust data cleaning and post list method to be implemented
        post_dict = dict(request.POST._iteritems())
        saved_list = []

        for list_item in post_dict['message_list']:
            data_dict = list_item['data']
            event_dict = list_item['event']
            message_dict = list_item['message']
            saved_data = api.Data.post(self.dj.deserialize(data_dict))
            event_dict['data'] = saved_data.id
            saved_event = api.Event.post(self.ej.deserialize(event_dict))
            message_dict['event'] = saved_event.id
            saved_list.append(api.Message.post(self.mj.deserialize(message_dict)))

        return JsonResponse(saved_list)

    def put(self):
        raise NotImplementedError


class MessageSingleView(View):
    def __init__(self):
        super().__init__()
        self.dj = jsonizer.DataJsonizer()
        self.ej = jsonizer.EventJsonizer()
        self.mj = jsonizer.MessageJsonizer()

    def delete(self, val):
        # TODO: Cascade delete to include data and event collections
        return JsonResponse(api.Message.delete(val=val))

    def get(self, val):
        return HttpResponse(self.mj.serialize(api.Message.get(val=val)), content_type="application/json")

    def patch(self, val, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        message_dict = post_dict['message']
        # TODO: Make query smarter
        saved_data = api.Data.patch(val=val, data=self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        # TODO: Make query smarter
        saved_event = api.Event.patch(val=val, data=self.ej.deserialize(event_dict))
        message_dict['event'] = saved_event.id
        saved_message = api.Message.patch(val=val, data=self.mj.deserialize(message_dict))

        return HttpResponse(self.mj.serialize(saved_message), content_type="application/json")

    def post(self, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        message_dict = post_dict['message']
        # TODO: Make query smarter
        saved_data = api.Data.post(self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        # TODO: Make query smarter
        saved_event = api.Event.post(self.ej.deserialize(event_dict))
        message_dict['event'] = saved_event.id
        saved_message = api.Message.post(self.mj.deserialize(message_dict))

        return HttpResponse(self.mj.serialize(saved_message), content_type="application/json")

    def put(self, pk, request):
        # TODO: Fix with helper function
        post_dict = dict(request.POST._iteritems())
        data_dict = post_dict['data']
        event_dict = post_dict['event']
        message_dict = post_dict['message']
        # TODO: Make query smarter
        saved_data = api.Data.put(pk=pk, data=self.dj.deserialize(data_dict))
        event_dict['data'] = saved_data.id
        # TODO: Make query smarter
        saved_event = api.Event.put(pk=pk, data=self.ej.deserialize(event_dict))
        message_dict['event'] = saved_event.id
        saved_message = api.Message.put(pk=pk, data=self.mj.deserialize(message_dict))

        return HttpResponse(self.mj.serialize(saved_message), content_type="application/json")

