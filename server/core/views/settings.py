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

from server.contrib.multiauth import logout
from server.contrib.multiauth.decorators import login_required
from server.contrib.pytoolbox.collections import update
from server.contrib.pytoolbox.django.forms import AllowEmptyMixin
from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import AcceptedTypesMixin, FormMixin
from server.core.api import SignalApi
from server.core.documents import Permission, Settings, Signal
from server.core.fields import PasswordField


class AccountView(View):
    template_name = 'core/settings/account.html'
    title = 'Account Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
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


class BaseView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return redirect_by_name('settings:profile')


class BillingView(View):
    template_name = 'core/settings/billing.html'
    title = 'Billing Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class ConnectionsView(View):
    template_name = 'core/settings/connections.html'
    title = 'Connection Settings'
    json_schema = {
        'type': 'object',
        'properties': {
            'signal_id': {
                'type': 'string',
            },
            'name': {
                'type': 'string'
            },
            'enabled': {
                'type': 'boolean'
            },
            'event_sources': {
                'type': 'object'
            }
        }
    }

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        signals = list(SignalApi.get(Q(user_id=request.user.id) & Q(complete=True)))
        signal_data = []

        for signal in signals:
            permissions = []

            for event_source_name, event_source in signal.provider.event_sources.items():
                name = event_source.name
                permissions.append({
                    'name': name,
                    'display_name': event_source.display_name,
                    'description': event_source.description,
                    'enabled': name in signal.permissions and signal.permissions[name].enabled
                })

            signal_data.append({
                'id': str(signal.id),
                'name': signal.name,
                'provider': {
                    'id': signal.provider.id,
                    'name': signal.provider.name
                },
                'enabled': signal.enabled,
                'permissions': permissions,
                'last_run': signal.last_run
            })

        return render(request, self.template_name, {
            'title': self.title,
            'signals': signal_data
        })

    def patch(self, request):
        # {
        #     "signal_id": "5987293847sdflkjsdf87",
        #     "name": "sample_signal",
        #     "enabled": true,
        #     "event_sources": {
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

        event_sources = deserialized.get('event_sources')

        if event_sources:
            schema = {
                'type': 'boolean'
            }

            for event_source, enabled in event_sources.items():
                try:
                    jsonschema.validate(enabled, schema)
                except jsonschema.ValidationError as err:
                    return HttpResponseBadRequest(err.message)

        signal_id = deserialized['signal_id']
        signal = Signal.objects.get(id=signal_id)

        if 'name' in deserialized:
            signal['name'] = deserialized.get('name')

        if 'enabled' in deserialized:
            signal['enabled'] = deserialized.get('enabled')

        if 'event_sources' in deserialized:
            for event_source_name in event_sources:
                # If the Permission exists, update its enabled status based on what was passed to the server
                if event_source_name in signal.permissions:
                    signal['permissions'][event_source_name]['enabled'] = event_sources[event_source_name]
                # If the Permission does not exist, then create it.  As part of the creation process, endpoint_data
                # for each endpoint that the associated event source might call also needs to be added to the signal,
                # and any default parameters for those endpoints need to be hydrated.
                else:
                    provider = signal.provider
                    this_event_source = provider['event_sources'][event_source_name]

                    new_permission = Permission(
                        enabled=True,
                        event_source=this_event_source
                    )

                    signal.permissions[event_source_name] = new_permission
                    signal.endpoint_data[event_source_name] = {}

                    for endpoint in this_event_source['endpoints']:
                        signal.endpoint_data[event_source_name][endpoint] = {}

                        for parameter in this_event_source['endpoints'][endpoint]['parameter_descriptions']:
                            this_parameter = this_event_source['endpoints'][endpoint]['parameter_descriptions'][parameter]

                            if 'default' in this_parameter.keys():
                                if this_parameter['default'] == 'date_now':
                                    signal.endpoint_data[event_source_name][endpoint][parameter] = datetime.date.today().isoformat().replace('-', '/')
                                else:
                                    signal.endpoint_data[event_source_name][endpoint][parameter] = this_parameter['default']

        SignalApi.put(signal_id, signal)

        return HttpResponse(status=204)


class EmailsView(View, AcceptedTypesMixin):
    template_name = 'core/settings/emails.html'
    title = 'Email Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class LocationView(View, FormMixin):
    template_name = 'core/settings/location.html'
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
    template_name = 'core/settings/notifications.html'
    title = 'Notification Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })


class ProfileView(View, AcceptedTypesMixin, FormMixin):
    template_name = 'core/settings/profile.html'
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
            'form': form
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
    template_name = 'core/settings/security.html'
    title = 'Security Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user,
            'title': self.title,
            'lockwidth_override': True
        })
