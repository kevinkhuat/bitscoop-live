import json

import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa

from example.app.decorators import render_to


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


@render_to('home.html')
def home(request):
    return context()


@login_required
@render_to('home.html')
def done(request):
    """Login complete view, displays user data"""
    return context()


@render_to('home.html')
def validation_sent(request):
    return context(
        validation_sent=True,
        email=request.session.get('email_validation_address')
    )


@render_to('home.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
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


@login_required
def ajax_auth_call(request, backend):
    if request.user.is_authenticated():
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
        return context()
    return context()


def ajax_logged_in_backends(request):
    if request.user.is_authenticated():
        backend_list = []
        for e in list(request.user.social_auth.all()):
            backend_list.append({'id': e.id, 'provider': e.provider})
        return HttpResponse(json.dumps(backend_list), content_type='application/json')
    return context()

# TODO: Fix custom scope to work here
# Todo: Remove to other library.
class CustomOScopeAuth2(BaseOAuth2):
    def get_scope(self, scope):
        scope = super(BaseOAuth2, self).get_scope()
        if self.data.get('extrascope'):
            scope = scope
        return scope


