import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from ografy.contrib.multiauth.decorators import login_required
from ografy.contrib.pytoolbox.django.response import redirect_by_name
from ografy.core.forms import LoginForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        return render(request, 'core/login.html', {
            'title': 'Login'
        })

    def post(self, request):
        user = None
        form = LoginForm(request.POST)
        form.full_clean()

        if form.is_valid():
            user = authenticate(**form.cleaned_data)

        if user is None:
            form.add_error(None, 'Invalid username or password.')

            return render(request, 'core/login.html', {
                'title': 'Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })
        else:
            login(request, user)

            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

            if not user.is_active:
                user.is_active = True
                user.save()

            return redirect_by_name('home')


class SudoView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SudoView, self).dispatch(*args, **kwargs)

    def post(self, request):
        return HttpResponse('', status=200)


def logout(request):
    auth_logout(request)

    return redirect_by_name('home')


@login_required
def mapbox_token(request):
    data = {
        'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
    }

    return HttpResponse(json.dumps(data), content_type='application/json')
