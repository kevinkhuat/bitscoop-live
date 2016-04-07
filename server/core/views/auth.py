from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.forms import Form as BaseForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from server.contrib.multiauth.decorators import login_required
from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import FormMixin


class LoginView(View, FormMixin):
    class Form(BaseForm):
        identifier = forms.CharField()
        password = forms.CharField()
        remember_me = forms.BooleanField(required=False)

    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        return render(request, 'login.html', {
            'title': 'Login'
        })

    def post(self, request):
        user = None
        form = self.get_filled_form(request)

        if 'cookieconsent' not in request.COOKIES:
            form.add_error(None, 'You must accept BitScoop\'s cookie policy to log in.')

            return render(request, 'login.html', {
                'title': 'Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })

        if form.is_valid():
            user = authenticate(**form.cleaned_data)

        if user is None:
            form.add_error(None, 'Invalid username or password.')

            return render(request, 'login.html', {
                'title': 'Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })
        else:
            login(request, user)

            remember_me = form.cleaned_data.get('remember_me', False)

            if not remember_me:
                request.session.set_expiry(0)

            if not user.is_active:
                user.is_active = True
                user.save()

            return redirect_by_name('home')


class LogoutView(View):
    def get(self, request):
        auth_logout(request)

        return redirect_by_name('home')


class MapboxTokenView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        data = {
            'MAPBOX_USER_NAME': settings.MAPBOX_USER_NAME,
            'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
        }

        return JsonResponse(data)


class SudoView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        return HttpResponse('', status=200)
