from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from ografy.apps.account.forms import UpdateDetailsForm, UpdatePasswordForm
from ografy.util import update
from ografy.util.response import redirect_by_name


@login_required
def index(request):
    return render(request, 'account/index.html', {
        'title': 'Ografy - Account'
    })


class DetailsView(View):
    template_name = 'account/details.html'
    title = 'Ografy - Update Details'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailsView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = UpdateDetailsForm({
            'email': user.email,
            'handle': user.handle,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

        return render(request, self.template_name, {
            'title': self.title,
            'form': form
        })

    def post(self, request):
        User = get_user_model()

        user = request.user
        form = UpdateDetailsForm(request.POST)
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
            update(user, **form.cleaned_data)
            user.save()

            return redirect_by_name('account_index')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'form': form
            })


class PasswordView(View):
    template_name = 'account/password.html'
    title = 'Ografy - Update Password'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
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

            return redirect_by_name('account_index')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'form': form
            })
