import json
import os

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from mongoengine import Q
from social.apps.django_app.default.models import UserSocialAuth

from ografy.apps.core.api import AuthorizedEndpointApi, EndpointDefinitionApi, ProviderApi, SignalApi
from ografy.apps.core.documents import AuthorizedEndpoint, EndpointDefinition

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
                if backend.uid == signal.psa_backend_uid:
                    unassociated_backends.remove(backend)

        # TODO: Change to bulk delete
        for signal in unverified_signals:
            SignalApi.delete(val=signal.id)

        for backend in unassociated_backends:
            UserSocialAuth.objects.get(uid=backend.uid).delete()

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
                'title': 'Ografy - Authorize ' + signal.provider.backend_name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal
            })
        else:
            if not signal.complete:
                initial_verification = True
                extra_data = UserSocialAuth.objects.filter(user_id=request.user.id, uid=signal.psa_backend_uid)[0].extra_data
                if signal.provider.auth_type == 1:
                    access_token = extra_data['access_token']
                    signal.oauth_token = access_token['oauth_token']
                    signal.oauth_token_secret = access_token['oauth_token_secret']
                elif signal.provider.auth_type == 0:
                    signal.access_token = extra_data['access_token']
                else:
                    pass
                signal.save()

            for endpoint in endpoint_list:
                pass
            return render(request, 'core/signals/verify.html', {
                'title': 'Ografy - Verify ' + signal.provider.backend_name + ' Connection',  # Change to signal
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
        signal.name = request.POST['name']
        signal.frequency = int(request.POST['updateFrequency'])
        signal.save()

        # FIXME: Right now the order of Authorized Endpoint enabled statuses on the Verification page is assumed
        # to be the same as the order that Authorized Endpoints are stored on the server, and it's also
        # assumed that the data will post to the server in the same order.
        # This will almost certainly not be the case, and some sort of input validation needs to be implemented.
        authorizedEndpointsEnabledList = json.loads(request.POST['authorizedEndpointsEnabledList'])
        # # For now, i is the index of both the input enabled list and the endpoints returned from the DB.
        # # This loops through each endpoint and sets its enabled field based on what was sent from the client.
        for index in authorizedEndpointsEnabledList:
            this_endpoint_dict = authorizedEndpointsEnabledList[index]
            this_authorized_endpoint_id = list(this_endpoint_dict.keys())[0]
            if not this_authorized_endpoint_id == 'None':
                AuthorizedEndpointApi.patch(this_authorized_endpoint_id, {
                    "enabled": this_endpoint_dict[this_authorized_endpoint_id]
                })
            else:
                if this_endpoint_dict[this_authorized_endpoint_id] == True:
                    this_endpoint = EndpointDefinitionApi.get(Q(id=index)).get()
                    new_authorized_endpoint = AuthorizedEndpoint(
                        name=this_endpoint.name,
                        route=os.path.join(this_endpoint.provider.base_route, this_endpoint.route_end),
                        provider=this_endpoint.provider,
                        user_id=request.user.id,
                        signal=signal,
                        endpoint_definition=this_endpoint,
                        enabled=True
                    )
                    AuthorizedEndpointApi.post(new_authorized_endpoint)

        # FIXME: Remove json.dumps and make sure to set the dataType to NOT json on the ajax request
        return HttpResponse(reverse('core_settings_signals'))
