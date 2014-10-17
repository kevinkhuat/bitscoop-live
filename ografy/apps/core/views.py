from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, get_user_model, login, logout as auth_logout
from django.shortcuts import redirect, render
from django.views.generic import View

from ografy.apps.core.forms import LoginForm, SignUpForm


def index(request):
    if request.user.is_authenticated():
        template = 'core/home.html'
        context = {
            'title': 'Ografy - Home'
        }
    else:
        template = 'core/index.html'
        context = {
            'title': 'Ografy',
            'content_class': 'no-vertical-pad'
        }

    return render(request, template, context)


class LoginView(View):
    def get(self, request):
        return render(request, 'core/login.html', {
            'title': 'Ografy - Login'
        })

    def post(self, request):
        user = None
        form = LoginForm(request.POST)
        form.full_clean()

        if form.is_valid():
            user = authenticate(**form.cleaned_data)

        if user is None:
            form.add_error('Invalid username or password.')

            return render(request, 'core/login.html', {
                'title': 'Ografy - Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })
        else:
            login(request, user)

            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(settings.SESSION_LIMIT)

            return redirect(reverse('core_index'))


def logout(request):
    auth_logout(request)

    return redirect(reverse('core_index'))


class SignupView(View):
    def get(self, request):
        return render(request, 'core/signup.html', {
            'title': 'Ografy - Sign Up'
        })

    def post(self, request):
        User = get_user_model()

        user = None
        form = SignUpForm(request.POST)
        form.full_clean()

        email = form.cleaned_data.get('email')
        if email is not None:
            email_count = User.objects.by_identifier(email).count()
            if email_count > 0:
                form.add_error('Email is in use.', field='email')

        handle = form.cleaned_data.get('handle')
        if handle is not None:
            handle_count = User.objects.by_identifier(handle).count()
            if handle_count > 0:
                form.add_error('Handle is in use.', field='handle')

        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(identifier=user.email, password=form.cleaned_data.get('password'))

        if user is None:
            return render(request, 'core/signup.html', {
                'title': 'Ografy - Signup',
                'form': form,
                'autofocus': 'username' in form.cleaned_data
            })
        else:
            login(request, user)

            return redirect(reverse('core_index'))


def contact(request):
    return render(request, 'core/contact.html', {
        'title': 'Ografy - Contact'
    })
