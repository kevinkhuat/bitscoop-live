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
from example.app.models import Account


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


# import requests
#
# user = User.objects.get(...)
# social = user.social_auth.get(provider='google-oauth2')
# response = requests.get(
# 'https://www.googleapis.com/plus/v1/people/me/people/visible',
# params={'access_token': social.extra_data['access_token']}
# )
# friends = response.json()['items']

@login_required
def ajax_auth_call(request, backend):
    user = Account.objects.get(request.REQUEST.get('user_id'))
    provider = request.REQUEST.get('provider')
    url = request.REQUEST.get('api_call_url')
    social = Account.social_auth.get(provider=provider)

    # TODO: Fix custom scope to work here

    response = requests.get(
        url, params={'access_token': social.extra_data['access_token']}
    )
    return response.json()

def ajax_logged_in_backends(request):
    if request.user.is_authenticated():
        user = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
        backends = Account.social_auth.get(user=user)
        return backends.json()
    return context()


# TODO: Fix custom scope to work here
# Todo: Remove to other library.
class CustomOScopeAuth2(BaseOAuth2):
    def get_scope(self, scope):
        scope = super(BaseOAuth2, self).get_scope()
        if self.data.get('extrascope'):
            scope = scope
        return scope


