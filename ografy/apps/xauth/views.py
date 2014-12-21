import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from social.apps.django_app.utils import psa
from social.backends.oauth import BaseOAuth1, BaseOAuth2

from ografy.apps.core.models import Signal, Provider

# TODO: Fix comments

@psa('social:complete')
def associate(request, backend):
    """This rest call endpoint complete the authorization workflow and have the server associate a signal with the logged in user.
    For this function to run properly, the application must start the Oauth 1/2/OpenID workflow and an authorization
    callback must be received from the signal's API by the server.

    #. *request* a request object must contain the variables:

        #. access_token
        #. access_token_secret

    #. *backend* the name of the backend

    * returns: returns the user who the backend signal was associated with or an error.
    """

    try:
        if isinstance(request.backend, BaseOAuth1):
            token = {
                'oauth_token': request.REQUEST.get('access_token'),
                'oauth_token_secret': request.REQUEST.get('access_token_secret'),
            }
        elif isinstance(request.backend, BaseOAuth2):
            token = request.REQUEST.get('access_token')
        else:
            return HttpResponseBadRequest('Wrong backend type')

        user = request.backend.do_auth(token, ajax=True)
        associated_provider = Provider.objects.get(backend_name=backend)
        associated_signal = Signal(user=user,
                                   provider=associated_provider,
                                   name=backend)
        associated_signal.save()

        ret = {'user_id': user.id,
               'username': user.username,
               'signal': associated_signal}

        return JsonResponse(ret)

    except requests.RequestException:
        return HttpResponseBadRequest()


@login_required
def call(request):
    """This rest endpoint will add an authorization signature to an API call and make the call on the server.

    #. *request* a request object must contain the variables:

        #. backend_id
        #. api_call_url

    #. *backend* the name of the backend

    * returns: returns the response from the call or an error.
    """

    # TODO: Make part of signals.js or Add functionality for known OAuth backends such as Steam to append developer keys as parameters for calls

    try:
        signal_id = request.REQUEST.get('signal_id', '')
        signal = Signal.objects.get(id=signal_id)
        api_call_url = request.REQUEST.get('api_call_url', '')
        backend_module = eval('social_backends.' + signal.provider.backend_name)
        social_auth = signal.get_social_auth()

        if hasattr(backend_module, 'BaseOAuth2'):
            response = requests.get(
                api_call_url, params={'access_token': social_auth.extra_data['access_token']}
            )
        elif hasattr(backend_module, 'BaseOAuth1'):
            response = requests.get(
                api_call_url, params={'access_token': social_auth.extra_data['access_token']}
            )
        else:
            response = requests.get(
                api_call_url
            )
        # response.content.user_id = request.user.id
        # response.content.username = request.user.email
        return HttpResponse(response)

    except requests.RequestException:
        return HttpResponseBadRequest()


@login_required
def signals(request):
    """This rest endpoint will be all logged in signal backends for the logged in user.

    * returns: returns the list of backends and their ids or an error.
    """

    try:
        return JsonResponse(Signal.get_social_auths_for_user(request.user))

    except requests.RequestException:
        return HttpResponseBadRequest()


@login_required
def proxy(request):
    """This rest endpoint will make an API call on the server.

    #. *request* a request object must contain the variable:

        #. api_call_url

    * returns: returns the response from the call or an error.
    """
    try:
        api_call_url = request.REQUEST.get('api_call_url', '')
        response = requests.get(api_call_url)

        return HttpResponse(response)

    except requests.RequestException:
        return HttpResponseBadRequest()


@login_required
def signature(request):
    """This rest endpoint will add an authorization signature to an API call and pass the access token for that call
    back to the client.

    #. *request* a request object must contain the variables:

        #. backend_id
        #. api_call_url

    #. *backend* the name of the backend

    * returns: returns the response from the call or an error.
    """

    try:
        signal_id = request.REQUEST.get('signal_id', '')
        api_call_url = request.REQUEST.get('api_call_url', '')

        signal = Signal.objects.get(id=signal_id)
        signed = {
            'api_call_url': api_call_url,
            'access_token': signal.get_user_social_auth().extra_data['access_token']
        }

        return JsonResponse(signed)

    except requests.RequestException:
        return HttpResponseBadRequest()
