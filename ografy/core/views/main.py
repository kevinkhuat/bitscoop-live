import json

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse, render
from django.utils.module_loading import import_module
from social.backends.utils import get_backend
from social.utils import module_member, setting_name

from ografy.core.documents import Signal
from ografy.settings import OGRAFY_MAPBOX_ACCESS_TOKEN


@login_required()
def main(request):
    template = 'core/main/main.html'

    return render(request, template, {
        'user': request.user
    })


@login_required()
def mapbox_token(request):
    data = {
        'OGRAFY_MAPBOX_ACCESS_TOKEN': OGRAFY_MAPBOX_ACCESS_TOKEN
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


BACKENDS = settings.AUTHENTICATION_BACKENDS

STORAGE = getattr(settings, setting_name('STORAGE'), 'social.apps.django_app.default.models.DjangoStorage')
Storage = module_member(STORAGE)

STRATEGY = getattr(settings, setting_name('STRATEGY'), 'social.strategies.django_strategy.DjangoStrategy')
Strategy = module_member(STRATEGY)


# FIXME: Huge security flaw, we do not verify any calls made on the server in any way!
@login_required()
def external_api_call(request):
    try:
        # Get associated signal
        signal_id = request.REQUEST.get('signal_id', '')
        signal = Signal.objects.get(id=signal_id)

        # Get API URL
        api_call_url = request.REQUEST.get('api_call_url', '')
        parameters = json.loads(request.REQUEST.get('parameters', ''))

        # Get the Backend
        backend_module = import_module('social.backends.{0}'.format(signal.provider.name.lower()))

        # Create a mock backend instance in order to use call signing libs in PSA
        redirect_uri = '/'
        backend_class = get_backend(BACKENDS, signal.provider.backend_name)
        loaded_backend = backend_class(Strategy(Storage), redirect_uri)

        # Case: OAuth 2 - 3 legged
        if hasattr(backend_module, 'BaseOAuth2'):
            # Find the access token location from the endpoint definition, currently assumes it's on the signals explicitly populated property
            token_location = parameters['access_token'].split('.')

            # If token is on the signal, slice the signal object to find the property
            if token_location[0] == 'signal':
                sliced = signal
                token_location.pop(0)
                for index in token_location:
                    sliced = sliced[index]
                parameters['access_token'] = sliced

            # TODO: else case where not on signal?

            # Call the API with the token in the header
            response = loaded_backend.get_json(
                api_call_url,
                params=parameters
            )

        # Case: OAuth 1 - 2 legged
        elif hasattr(backend_module, 'BaseOAuth1'):

            # TODO: Token & Token secret should eventually be coming from the signal and
            # should be mapped from the location specified on the endpoint definition just like OAuth 2

            for item in parameters:
                if item == 'oauth_token' or item == 'oauth_token_secret':
                    # Find the token location from the endpoint definition, currently assumes it's on the signals explicitly populated property
                    token_location = parameters[item].split('.')

                    # If token is on the signal, slice the signal object to find the property
                    if token_location[0] == 'signal':
                        sliced = signal
                        token_location.pop(0)
                        for index in token_location:
                            sliced = sliced[index]
                        parameters[item] = sliced

            response = loaded_backend.get_json(
                api_call_url,
                auth=loaded_backend.oauth_auth(parameters)
            )

        # Case: OpenId
        else:
            # Get key location from endpoint definition
            key_location = parameters['key'].split('.')

            # If token is on the signal, slice the signal object to find the property
            if key_location[0] == 'signal':
                sliced = signal
                key_location.pop(0)
                for index in key_location:
                    sliced = sliced[index]
                parameters['key'] = sliced

            # TODO: else case where not on signal?

            # Call the API with the token in the header
            response = loaded_backend.get_json(
                api_call_url,
                params=parameters
            )

        # TODO: Use simpleJson?
        return HttpResponse(json.dumps(response))

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
