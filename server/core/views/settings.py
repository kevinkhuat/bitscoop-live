import datetime
import json

import jsonschema
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import Form as BaseForm
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from mongoengine import Q
from django.http import Http404

from server.contrib.multiauth import logout
from server.contrib.multiauth.decorators import login_required
from server.contrib.pytoolbox import initialize_endpoint_data
from server.contrib.pytoolbox.collections import update
from server.contrib.pytoolbox.django.forms import AllowEmptyMixin
from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import AcceptedTypesMixin, FormMixin
from server.core.api import ConnectionApi
from server.core.documents import Connection, Permission, Settings
from server.core.fields import PasswordField


class AccountView(View):
    template_name = 'settings/account.html'
    title = 'Account Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title,
            'settings_type': 'Account'
        })


class AccountHandleView(View, FormMixin):
    class Form(BaseForm):
        handle = forms.CharField(
            max_length=20,
            required=False,
            validators=settings.HANDLE_VALIDATORS
        )

        def clean(self):
            cleaned_data = super().clean()
            handle = cleaned_data.get('handle')

            if handle:
                user_model = get_user_model()
                queryset = user_model.objects.filter(handle__iexact=handle)

                if hasattr(self, 'current_user'):
                    queryset = queryset.exclude(id=self.current_user.id)

                if queryset.count() > 0:
                    self.add_error('handle', 'Handle is in use.')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user
        form = self.get_filled_form(request)

        if form.is_valid():
            update(user, form.cleaned_data)
            user.save()
            response = JsonResponse(form.cleaned_data)
        else:
            response = JsonResponse(form.errors, status=422)

        return response


class AccountPasswordView(View, FormMixin):
    class Form(BaseForm):
        current_password = forms.CharField()
        new_password = PasswordField()
        new_password_repeated = forms.CharField()

        def clean(self):
            cleaned_data = super().clean()
            current_password = cleaned_data.get('current_password')
            new_password = cleaned_data.get('new_password')
            new_password_repeated = cleaned_data.get('new_password_repeated')

            if not self.current_user.check_password(current_password):
                self.add_error('current_password', 'Invalid password.')

            if new_password != new_password_repeated:
                self.add_error('new_password_repeated', 'Repeated password doesn\'t match.')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user
        form = self.get_filled_form(request)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.password_date = timezone.now()
            user.save()
            response = JsonResponse('', safe=False)
        else:
            response = JsonResponse(form.errors, status=422)

        return response


class AccountDeactivateView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        logout(request)

        return HttpResponse(status=204)


class AccountDeleteView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user

        logout(request)
        user.delete()

        return HttpResponse(status=204)


class BaseView(View):
    template_name = 'settings/base.html'
    title = 'Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return redirect_by_name('settings:profile')


class BillingView(View):
    template_name = 'settings/billing.html'
    title = 'Billing Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        raise Http404

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class ConnectionsView(View):
    template_name = 'settings/connections.html'
    title = 'Connection Settings'
    json_schema = {
        'type': 'object',
        'properties': {
            'connection_id': {
                'type': 'string',
            },
            'name': {
                'type': 'string'
            },
            'enabled': {
                'type': 'boolean'
            },
            'sources': {
                'type': 'object'
            }
        }
    }

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        connections = list(ConnectionApi.get(Q(user_id=request.user.id) & Q(auth_status__complete=True)))
        connection_data = []

        for connection in connections:
            permissions = []

            for source_name, source in connection.provider.sources.items():
                name = source_name
                permissions.append({
                    'name': name,
                    'source': source,
                    'enabled': name in connection.permissions and connection.permissions[name].enabled
                })

            connection_data.append({
                'id': str(connection.id),
                'name': connection.name,
                'provider': {
                    'id': connection.provider.id,
                    'name': connection.provider.name
                },
                'enabled': connection.enabled,
                'permissions': permissions,
                'last_run': connection.last_run
            })

        return render(request, self.template_name, {
            'title': self.title,
            'connections': connection_data,
            'settings_type': 'Connections'
        })

    def patch(self, request):
        # {
        #     "connection_id": "5987293847sdflkjsdf87",
        #     "name": "sample_connection",
        #     "enabled": true,
        #     "sources": {
        #         "sample_permission": true
        #     }
        # }

        try:
            decoded = request.body.decode('utf-8')
        except UnicodeDecodeError:
            return HttpResponseBadRequest('Invalid UTF-8 string.')

        try:
            deserialized = json.loads(decoded)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON.')

        try:
            jsonschema.validate(deserialized, self.json_schema)
        except jsonschema.ValidationError as err:
            return HttpResponseBadRequest(err.message)

        sources = deserialized.get('sources')

        if sources:
            schema = {
                'type': 'boolean'
            }

            for source, enabled in sources.items():
                try:
                    jsonschema.validate(enabled, schema)
                except jsonschema.ValidationError as err:
                    return HttpResponseBadRequest(err.message)

        connection_id = deserialized['connection_id']
        connection = Connection.objects.get(id=connection_id)

        if 'name' in deserialized:
            connection['name'] = deserialized.get('name')

        if 'enabled' in deserialized:
            connection['enabled'] = deserialized.get('enabled')

        if 'sources' in deserialized:
            for source_name in sources:
                # If the Permission exists, update its enabled status based on what was passed to the server
                if source_name in connection.permissions:
                    connection['permissions'][source_name]['enabled'] = sources[source_name]
                # If the Permission does not exist, then create it.  As part of the creation process, endpoint_data
                # for each endpoint that the associated event source might call also needs to be added to the connection,
                # and any default parameters for those endpoints need to be hydrated.
                else:
                    provider = connection.provider

                    new_permission = Permission(
                        enabled=True,
                        frequency=1
                    )

                    connection.permissions[source_name] = new_permission
                    connection.endpoint_data[source_name] = {}

                    initialize_endpoint_data(provider, connection, source_name, provider['sources'][source_name]['mapping'], provider['sources'][source_name]['population'])

        ConnectionApi.put(connection_id, connection)

        return HttpResponse(status=204)


class EmailsView(View, AcceptedTypesMixin):
    template_name = 'settings/emails.html'
    title = 'Email Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        raise Http404

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class LocationView(View, FormMixin):
    template_name = 'settings/location.html'
    title = 'Location Settings'

    class Form(AllowEmptyMixin, BaseForm):
        LOCATION_ESTIMATION_METHOD = (
            ('Last', 'Last known location'),
            ('Next', 'Next known location'),
            ('Closest', 'Closest location'),
            ('Between', 'Interpolate between last and next'),
        )

        allow_location_collection = forms.BooleanField(required=False)
        location_estimation_method = forms.ChoiceField(choices=LOCATION_ESTIMATION_METHOD)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        raise Http404

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        settings = Settings.objects.get(user_id=user.id)

        next_estimate_date = settings.last_estimate_all_locations + datetime.timedelta(days=5)
        new_estimate_allowed = datetime.datetime.now() > next_estimate_date

        return render(request, self.template_name, {
            'title': self.title,
            'next_estimate_date': next_estimate_date,
            'new_estimate_allowed': new_estimate_allowed,
            'settings': settings,
            'user': user
        })

    def patch(self, request):
        form = self.get_filled_form(request, empty_permitted=True)

        if form.is_valid():
            user = request.user
            settings = Settings.objects.get(user_id=user.id)
            update(settings, form.cleaned_data)
            settings.save()

            response = JsonResponse(form.cleaned_data)
        else:
            response = JsonResponse(form.errors, status=422)

        return response


class NotificationsView(View):
    template_name = 'settings/notifications.html'
    title = 'Notification Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        raise Http404

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class ProfileView(View, AcceptedTypesMixin, FormMixin):
    template_name = 'settings/profile.html'
    title = 'Profile Settings'
    accepted_types = {'application/json'}

    class Form(AllowEmptyMixin, BaseForm):
        first_name = forms.CharField(max_length=30, required=False)
        last_name = forms.CharField(max_length=30, required=False)
        email = forms.EmailField(max_length=256)
        gender = forms.CharField(max_length=20, required=False)
        other_gender = forms.CharField(max_length=20, required=False)
        birthday = forms.DateField(required=False)

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get('email')
            other_gender = cleaned_data.get('other_gender')

            if email:
                user_model = get_user_model()
                queryset = user_model.objects.filter(email__iexact=email)

                if hasattr(self, 'current_user'):
                    queryset = queryset.exclude(id=self.current_user.id)

                email_count = queryset.count()

                if email_count > 0:
                    self.add_error('email', 'Email is in use.')

            if other_gender:
                self.cleaned_data['gender'] = other_gender

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = self.Form({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birthday': user.birthday,
            'gender': user.gender
        })
        form.current_user = request.user

        return render(request, self.template_name, {
            'title': self.title,
            'form': form,
            'settings_type': 'Profile'
        })

    def put(self, request):
        form = self.get_filled_form(request, empty_permitted=False)
        content_type = self.get_content_type(request)
        code = 200

        if form.is_valid():
            user = request.user
            update(user, form.cleaned_data)
            user.save()
        else:
            code = 422

        if content_type == 'text/html':
            response = render(request, self.template_name, {
                'title': self.title,
                'form': form
            }, status=code)
        else:
            if form.is_valid():
                response = JsonResponse(form.cleaned_data, status=code)
            else:
                response = JsonResponse(form.errors, status=code)

        return response

    def patch(self, request):
        form = self.get_filled_form(request, empty_permitted=True)

        if form.is_valid():
            user = request.user
            update(user, form.cleaned_data)
            user.save()

            response = JsonResponse(form.cleaned_data)
        else:
            response = JsonResponse(form.errors, status=422)

        return response


class SecurityView(View):
    template_name = 'settings/security.html'
    title = 'Security Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        raise Http404

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user,
            'title': self.title,
            'lockwidth_override': True
        })
