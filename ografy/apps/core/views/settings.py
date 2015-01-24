from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from ografy.apps.core.forms import UpdatePersonalForm, UpdatePasswordForm
from ografy.util.collections import update
from ografy.util.response import redirect_by_name

from ografy.apps.core import api as core_api


class PersonalView(View):
    template_name = 'core/settings/personal.html'
    title = 'Ografy - Update Personal Information'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonalView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = UpdatePersonalForm({'email': user.email, # 'handle': user.handle,
            'first_name': user.first_name, 'last_name': user.last_name})

        return render(request, self.template_name, {'title': self.title, 'form': form})

    def post(self, request):
        User = get_user_model()

        user = request.user
        form = UpdatePersonalForm(request.POST)
        form.full_clean()

        email = form.cleaned_data.get('email')
        if email is not None:
            email_count = User.objects.filter(email__iexact=email).exclude(id=user.id).count()
            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')
        if handle is not None:
            handle_count = User.objects.filter(handle__iexact=handle).exclude(id=user.id).count()
            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        if form.is_valid():
            update(user, form.cleaned_data)
            user.save()

            return redirect_by_name('core_settings_personal')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})


class SecurityView(View):
    template_name = 'core/settings/security.html'
    title = 'Ografy - Update Security Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SecurityView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'title': self.title})

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

            return redirect_by_name('core_settings_personal')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})


class SignalView(View):
    template_name = 'core/settings/signals.html'
    title = 'Ografy - Signals Settings'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SignalView, self).dispatch(*args, **kwargs)

    def get(self, request):
        signals = list(core_api.SignalApi.get(Q(user=request.user.id) | Q(complete=True)))
        verify_url = reverse('core_providers')

        return render(request, self.template_name, {
            'title': self.title,
            'signals': signals,
            'verify_url': verify_url
        })

@login_required
def base(request):
    return render(request, 'core/settings/personal.html', {'title': 'Ografy - Base'})
