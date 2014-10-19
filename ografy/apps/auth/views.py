import json
import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.template import Context
from django.views.generic import View
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.apps.django_app.utils import psa

from ografy.apps.auth.forms import LoginForm


# Ografy Account specific login/logout
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html', {
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

            return render(request, 'auth/login.html', {
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


# Python Social Auth Specific Workflow
@psa('social:complete')
def associate(request, backend):
    if request.user.is_authenticated():
        if isinstance(backend, BaseOAuth1):
            token = {
                'oauth_token': request.REQUEST.get('access_token'),
                'oauth_token_secret': request.REQUEST.get('access_token_secret'),
            }
        elif isinstance(request.backend, BaseOAuth2):
            token = request.REQUEST.get('access_token')
        else:
            raise HttpResponseBadRequest('Wrong backend type')

        user = request.backend.do_auth(token, ajax=True)
        login(request, user)
        data = {'id': user.id, 'username': user.username}

        return HttpResponse(json.dumps(data), mimetype='application/json')

    return Context()

@login_required
def call(request, backend):
    backend_id = request.REQUEST.get('backend_id', '')
    api_call_url = request.REQUEST.get('api_call_url', '')

    if backend_id:
        social = request.user.social_auth.get(id=backend_id, provider=backend)
        response = requests.get(
            api_call_url, params={'access_token': social.extra_data['access_token']}
        )
        # response.content.user_id = request.user.id
        # response.content.username = request.user.email
        return HttpResponse(response)

    return Context()

@login_required
def signals(request):
    backend_list = []

    for e in list(request.user.social_auth.all()):
        backend_list.append({
            'id': e.id,
            'provider': e.provider
        })

    return HttpResponse(json.dumps(backend_list), content_type='application/json')

@login_required
def proxy(request):
    api_call_url = request.REQUEST.get('api_call_url', '')
    response = requests.get(api_call_url)

    return HttpResponse(response)

@login_required
def signature(request, backend):
    backend_id = request.REQUEST.get('backend_id', '')
    api_call_url = request.REQUEST.get('api_call_url', '')

    if backend_id:
        social = request.user.social_auth.get(id=backend_id, provider=backend)
        signed = {
            'api_call_url': api_call_url,
            'access_token': social.extra_data['access_token']
        }

        return HttpResponse(signed)

    return Context()
