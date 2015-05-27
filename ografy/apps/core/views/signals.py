import json
import os

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from mongoengine import Q
from social.apps.django_app.default.models import UserSocialAuth

from ografy.apps.core.api import AuthorizedEndpointApi, EndpointDefinitionApi, ProviderApi, SignalApi
from ografy.apps.core.documents import AuthorizedEndpoint

@login_required
def authorize(request):
    # # Look up signals from API for current user where signal
    # # is not verified or complete.
    unassociated_backends = list(UserSocialAuth.objects.filter(user=request.user))
    unverified_signals = list(SignalApi.get(val=Q(user_id=request.user.id) & (Q(complete=False) | Q(connected=False))))

    signal_count = len(unverified_signals)

    # If there is more than one unverified+incomplete signal,
    # delete all and start over.
    if signal_count == 0 or signal_count > 1:
        for signal in unverified_signals:
            for backend in unassociated_backends:
                if backend.id == signal.usa_id:
                    unassociated_backends.remove(backend)

        # TODO: Change to bulk delete
        for signal in unverified_signals:
            SignalApi.delete(val=signal.id)

        for backend in unassociated_backends:
            UserSocialAuth.objects.get(id=backend.id).delete()

        return HttpResponseRedirect(reverse('core_providers'))

    else:
        signal = unverified_signals[0]

        return HttpResponseRedirect(reverse('core_verify', kwargs={'pk': signal.id}))

    # # Messed up signals
    # return render(request, 'core/signals/authorize.html', {
    #     'title': 'Ografy - Authorize ' + signal.name + ' Connection',  # Change to signal
    #     'content_class': 'left',
    #     'signal': signal
    # })


@login_required
def connect(request, pk):
    provider = ProviderApi.get(Q(id=pk)).get()

    return render(request, 'core/signals/connect.html', {
        'title': 'Ografy - Connect to ' + provider.name,
        'content_class': 'left',
        'provider': provider,
        'flex_override': True,
        'user_id': request.user.id,
        'postback_url': reverse('core_authorize')
    })

@login_required
def connect_name(request, name):
    provider = ProviderApi.get(Q(backend_name=name)).get()

    return HttpResponseRedirect(reverse('core_connect', kwargs={'pk': provider.id}))

@login_required
def providers(request):
    providers = list(ProviderApi.get())
    signal_by_user = Q(user_id=request.user.id)
    signals = SignalApi.get(val=signal_by_user)
    connect_url = reverse('core_providers')

    # FIXME: Make the count happen in the DB
    for provider in providers:
        for signal in signals:
            if provider.id == signal.provider.id:
                provider.associated_signal = True
                if hasattr(provider, 'assoc_count'):
                    provider.assoc_count += 1
                else:
                    provider.assoc_count = 1

    return render(request, 'core/signals/providers.html', {
        'title': 'Ografy - Providers',
        'body_class': 'full',
        'left_class': 'bordered right',
        'providers_override': True,
        'providers': providers,
        'connect_url': connect_url
    })

@login_required
def verify(request, pk):
    if request.method == 'GET':
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=pk)).get()
        endpoint_definitions = EndpointDefinitionApi.get(Q(provider=signal.provider.id))
        authorized_endpoints = AuthorizedEndpointApi.get(Q(signal=signal.id))
        initial_verification = False
        endpoint_list = {}
        for endpoint_definition in endpoint_definitions:
            matched_auth_endpoint = False
            for authorized_endpoint in authorized_endpoints:
                if authorized_endpoint.endpoint_definition.id == endpoint_definition.id:
                    matched_auth_endpoint = True
                    endpoint_list[endpoint_definition] = authorized_endpoint
            if not matched_auth_endpoint:
                endpoint_list[endpoint_definition] = None

        if signal.connected is False:
            return render(request, 'core/signals/authorize.html', {
                'title': 'Ografy - Authorize ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal
            })
        else:
            if not signal.complete:
                initial_verification = True
                extra_data = UserSocialAuth.objects.filter(user_id=request.user.id, id=signal.usa_id)[0].extra_data
                if signal.provider.auth_type == 1:
                    access_token = extra_data['access_token']
                    signal.oauth_token = access_token['oauth_token']
                    signal.oauth_token_secret = access_token['oauth_token_secret']
                elif signal.provider.auth_type == 0:
                    signal.access_token = extra_data['access_token']
                signal.save()

            for endpoint in endpoint_list:
                pass
            return render(request, 'core/signals/verify.html', {
                'title': 'Ografy - Verify ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal,
                'initial_verification': initial_verification,
                'endpoint_list': endpoint_list
            })
    elif request.method == 'POST':
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=pk)).get()
        if (not signal.complete):
            signal.complete = True
            signal.enabled = True
        user_social_auth_instance = list(UserSocialAuth.objects.filter(id=signal.usa_id))[0]
        signal.name = request.POST['name']
        signal.frequency = int(request.POST['updateFrequency'])
        extra_data = user_social_auth_instance.extra_data
        #OAuth1 returns tokens on extra_data.  Signal.extra_data is serialized and sent to the user, and we don't
        #want those tokens available on the client, so delete them from signal.extra_data
        if 'access_token' in extra_data:
            if 'oauth_token' in extra_data['access_token']:
                extra_data['access_token'].pop('oauth_token')
                extra_data['access_token'].pop('oauth_token_secret')
            else:
                extra_data.pop('access_token')
        signal.extra_data = extra_data
        signal.save()

        # This handles updating the Authorized Endpoints enabled status and the creation of Authorized Endpoints.
        # The client passes a dictionary of Endpoint Definitions and their associated Authorized Endpoints to the server.
        # The dictionary keys are the IDs of the Endpoint Definitions associated with this signal.
        # The dictionary values are either 'None' if an Authorized Endpoint has not been created for that endpoint
        # definition yet, or a dictionary if there is an Authorized Endpoint.
        # The sub-dictionary's key is the ID of the Authorized Endpoint, and the value is a boolean representing
        # whether or not the Authorized Endpoint is enabled.
        # Example:
        # {
        #   38920743: None,
        #   32957207: {
        #       38828502: False
        #   }
        # }
        # Endpoint definition 38920743 has no Authorized Endpoint associated with it.
        # Endpoint definition 32957207 has Authorized Endpoint 38828502 associated with it.
        # Authorized Endpoint 38828502 should be disabled.
        #

        # Get the endpoint dictionary from the request
        endpointsDict = json.loads(request.POST['endpointsDict'])
        for index in endpointsDict:
            # Get the Authorized Endpoint dictionary for this Endpoint Definition (or None if there is no Authorized Endpoint).
            this_endpoint_dict = endpointsDict[index]
            # Get the Authorized Endpoint ID (or None if it doesn't exist)
            this_authorized_endpoint_id = list(this_endpoint_dict.keys())[0]
            # If the Authorized Endpoint exists, update its enabled status based on what was passed to the server
            if not this_authorized_endpoint_id == 'None':
                AuthorizedEndpointApi.patch(this_authorized_endpoint_id, {
                    "enabled": this_endpoint_dict[this_authorized_endpoint_id]
                })
            else:
                # If the Authorized Endpoint does not exist and the user wants that endpoint to be used, create an Authorized Endpoint.
                if this_endpoint_dict[this_authorized_endpoint_id] == True:
                    this_endpoint = EndpointDefinitionApi.get(Q(id=index)).get()
                    route = ''
                    if this_endpoint.provider.backend_name == 'facebook':
                        route = os.path.join(os.path.join(this_endpoint.provider.base_route, signal.usa_id, this_endpoint.route_end))
                    else:
                        route = os.path.join(this_endpoint.provider.base_route, this_endpoint.route_end)

                    new_authorized_endpoint = AuthorizedEndpoint(
                        name=this_endpoint.name,
                        route=route,
                        provider=this_endpoint.provider,
                        user_id=request.user.id,
                        signal=signal,
                        endpoint_definition=this_endpoint,
                        enabled=True
                    )
                    AuthorizedEndpointApi.post(new_authorized_endpoint)

        return HttpResponse(reverse('core_settings_signals'))
