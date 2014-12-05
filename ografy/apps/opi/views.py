from django.views.generic import View


class DataView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DataSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class EventView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class EventSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class MessageView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class MessageSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, requset, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class ProviderView(View):
    def get(self, request):
        pass


class ProviderSingleView(View):
    def get(self, request, id):
        pass


class SettingsView(View):
    def get(self, request):
        pass

    def patch(self, request):
        pass


class SignalView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class SignalSingleView(View):
    def delete(self, request, id):
        pass

    def get(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def put(self, request, id):
        pass


class UserView(View):
    def get(self, request):
        pass


class UserSingleView(View):
    def get(self, request, id):
        pass
