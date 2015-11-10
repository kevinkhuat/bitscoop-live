from django.http import QueryDict

from server.contrib.pytoolbox.django import get_content_type


class AcceptedTypesMixin(object):
    def get_content_type(self, request):
        types = getattr(self, 'accepted_types', {'text/html'})
        default_type = getattr(self, 'default_type', 'text/html')

        return get_content_type(request.accepted_types, types, default_type)


class FormMixin(object):
    def get_filled_form(self, request, initial=None, empty_permitted=False):
        form_class = getattr(self, 'form_class', None)

        if not form_class:
            form_class = getattr(self, 'Form', None)

        if not form_class:
            return None

        inputs = QueryDict(request.body.decode('utf-8'))
        form = form_class(inputs, empty_permitted=empty_permitted, initial=initial)
        form.current_user = request.user

        return form
