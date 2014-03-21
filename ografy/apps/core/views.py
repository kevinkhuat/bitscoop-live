from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View

from ografy.apps.core.models import User


def index(request):
    if request.user.is_authenticated():
        template = 'core/home.html'
        context = {}
    else:
        template = 'core/index.html'
        context = {}

    return render(request, template, context)


class LoginView(View):
    def get(self, request):
        return render(request, 'core/login.html', {
            'title': 'Ografy - Login'
        })

    def post(self, request):
        user = authenticate(identifier=request.POST.get('identifier'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)

            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(settings.SESSION_LIMIT)

            return redirect(reverse('core_index'))
        else:
            return redirect(reverse('core_login'))


def logout(request):
    auth_logout(request)

    return redirect(reverse('core_index'))


class SignupView(View):
    def get(self, request):
        return render(request, 'core/signup.html', {
            'title': 'Ografy - Signup'
        })

    def post(self, request):
        user = User(
            email=request.POST.get('email'),
            handle=request.POST.get('handle', None),
            first_name=request.POST.get('first_name', None),
            last_name=request.POST.get('last_name', None)
        )
        user.set_password(request.POST.get('password'))
        user.save()

        user = authenticate(identifier=user.email, password=request.POST.get('password'))
        if user is not None:
            login(request, user)

        return redirect(reverse('core_index'))


def contact(request):
    return render(request, 'core/contact.html', {
        'title': 'Ografy - Contact'
    })
