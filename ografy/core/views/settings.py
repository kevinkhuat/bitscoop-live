import copy
import datetime
import json
import urllib

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from mongoengine import Q

from ografy.contrib.pytoolbox.collections import update
from ografy.contrib.pytoolbox.django.response import redirect_by_name
from ografy.core.api import EndpointApi, PermissionApi, SignalApi
from ografy.core.documents import Permission, Settings
from ografy.core.forms import UpdateAccountForm, UpdateLocationForm, UpdatePasswordForm


class AccountView(View):
    template_name = 'core/settings/account.html'
    title = 'Ografy - Update Account Information'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = UpdateAccountForm({
            'email': user.email,
            # 'handle': user.handle,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

        return render(request, self.template_name, {
            'title': self.title,
            'lockwidth_override': True,
            'form': form,
            'selected': 'account'
        })

    def post(self, request):
        user_model = get_user_model()

        user = request.user
        inputs = QueryDict(request.body.decode('utf-8'))
        form = UpdateAccountForm(inputs)
        form.full_clean()

        email = form.cleaned_data.get('email')
        if email is not None:
            email_count = user_model.objects.filter(email__iexact=email).exclude(id=user.id).count()

            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')
        if handle is not None:
            handle_count = user_model.objects.filter(handle__iexact=handle).exclude(id=user.id).count()

            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        if form.is_valid():
            update(user, form.cleaned_data)
            user.save()

            return redirect_by_name('core_settings_account')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'lockwidth_override': True,
                'form': form
            })

    def patch(self, request):
        user_model = get_user_model()

        user = request.user
        inputs = QueryDict(request.body.decode('utf-8'))
        form = UpdateAccountForm(inputs)
        form.full_clean()

        email = form.cleaned_data.get('email')

        if email is not None:
            email_count = user_model.objects.filter(email__iexact=email).exclude(id=user.id).count()
            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')

        if handle is not None:
            handle_count = user_model.objects.filter(handle__iexact=handle).exclude(id=user.id).count()
            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        partial_form = copy.deepcopy(form)

        for field in form.cleaned_data:
            if field not in form.changed_data:
                partial_form.cleaned_data.pop(field)

        if partial_form.is_valid():
            update(user, partial_form.cleaned_data)
            user.save()

            return HttpResponse(status=200)
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'lockwidth_override': True,
                'form': form
            })


class LocationView(View):
    template_name = 'core/settings/location.html'
    title = 'Ografy - Update Location Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LocationView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        settings = Settings.objects.get(user_id=user.id)

        next_estimate_date = settings.last_estimate_all_locations + datetime.timedelta(days=5)
        new_estimate_allowed = datetime.datetime.now() > next_estimate_date

        return render(request, self.template_name, {
            'title': self.title,
            'lockwidth_override': True,
            'next_estimate_date': next_estimate_date,
            'new_estimate_allowed': new_estimate_allowed,
            'settings': settings,
            'selected': 'location',
            'user': user
        })

    def patch(self, request):
        user = request.user
        settings = Settings.objects.get(user_id=user.id)

        inputs = QueryDict(request.body.decode('utf-8'))
        form = UpdateLocationForm(inputs)
        form.full_clean()

        # Remove allow_location_estimation from form.cleaned_data if location_estimation_method is the field being
        # updated.

        if 'location_estimation_method' in form.changed_data:
            form.cleaned_data.pop('allow_location_collection')
        else:
            form.cleaned_data.pop('location_estimation_method')

        if form.is_valid():
            update(settings, form.cleaned_data)
            settings.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse({'form': form}, content_type='json', status=400)


class SecurityView(View):
    template_name = 'core/settings/security.html'
    title = 'Ografy - Update Security Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SecurityView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user,
            'title': self.title,
            'lockwidth_override': True,
            'selected': 'security',
        })

    def post(self, request):
        user = request.user
        form = UpdatePasswordForm(request.POST)
        form.full_clean()

        if not request.user.check_password(form.cleaned_data['password']):
            form.add_error('password', 'Invalid password.')

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.password_date = timezone.now()
            user.save()

            return redirect_by_name('core_settings_account')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'lockwidth_override': True,
                'form': form
            })


class SignalView(View):
    template_name = 'core/settings/signals.html'
    title = 'Ografy - Signals Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SignalView, self).dispatch(*args, **kwargs)

    def get(self, request):
        signals = list(SignalApi.get(Q(user_id=request.user.id) & Q(complete=True)))

        for signal in signals:
            signal.endpoint_list = {}
            endpoints = EndpointApi.get(Q(provider=signal.provider.id))
            permissions = PermissionApi.get(Q(signal=signal.id))

            for endpoint in endpoints:
                matched_auth_endpoint = False

                for permission in permissions:
                    if permission.endpoint.id == endpoint.id:
                        matched_auth_endpoint = True
                        signal.endpoint_list[endpoint] = permission

                if not matched_auth_endpoint:
                    signal.endpoint_list[endpoint] = None

        return render(request, self.template_name, {
            'title': self.title,
            'signals': signals,
            'lockwidth_override': True,
            'selected': 'signal'
        })

    def post(self, request):
        signal_id = request.POST['signal_id']
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=signal_id)).get()
        enabled = json.loads(request.POST['enabled'])
        this_endpoint_id = request.POST['endpoint_id']
        # Get the Permission ID (or None if it doesn't exist)
        this_permission_id = request.POST['permission_id']
        # If the Permission exists, update its enabled status based on what was passed to the server

        if not this_permission_id == 'None':
            return_permission = PermissionApi.patch(this_permission_id, {
                "enabled": enabled
            })
        else:
            this_endpoint = EndpointApi.get(Q(id=this_endpoint_id)).get()
            url_parts = [''] * 6

            url_parts[0] = this_endpoint.provider.scheme
            url_parts[1] = this_endpoint.provider.domain
            url_parts[2] = this_endpoint.path

            if this_endpoint.provider.backend_name == 'facebook':
                url_parts[3] = signal.usa_id
                # This was the old way of joining, leaving in for reference until this is locked
                # route = os.path.join(os.path.join(this_endpoint.provider.base_route, signal.usa_id, this_endpoint.path))

            route = urllib.parse.urlunparse(url_parts)

            new_permission = Permission(
                name=this_endpoint.name,
                route=route,
                provider=this_endpoint.provider,
                user_id=request.user.id,
                signal=signal,
                endpoint=this_endpoint,
                enabled=True
            )
            return_permission = PermissionApi.post(new_permission)

        return HttpResponse(str(return_permission.id), content_type='application/json')

    def delete(self, request):
        signal_id = request.POST['signal_id']
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=signal_id)).get()


@login_required
def base(request):
    return render(request, 'core/settings/account.html', {
        'title': 'Ografy - Base',
        'lockwidth_override': True
    })
