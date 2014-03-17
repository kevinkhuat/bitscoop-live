from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View


def index(request):
    if request.user.is_authenticated():
        print('authenticated view')
        template = 'core/index.html'
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
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(settings.SESSION_LIMIT)

        return redirect(reverse('core_index'))


def logout(request):
    auth_logout(request)

    return redirect(reverse('core_index'))
