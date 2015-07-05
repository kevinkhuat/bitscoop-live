import json
import urllib

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from mongoengine import Q
from social.apps.django_app.default.models import UserSocialAuth

from ografy.core.api import EndpointApi, PermissionApi, ProviderApi, SignalApi
from ografy.core.documents import Permission


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
def connect(request, name):
    expression = Q(url_name=name)
    provider = ProviderApi.get(expression).get()

    return render(request, 'core/signals/connect.html', {
        'title': 'Ografy - Connect to ' + provider.name,
        'content_class': 'left',
        'provider': provider,
        'flex_override': True,
        'user': request.user.id,
        'current': 'connect',
        'postback_url': reverse('core_authorize')
    })


@login_required
def providers(request):
    providers = list(ProviderApi.get())
    signal_by_user = Q(user_id=request.user.id)
    signals = SignalApi.get(val=signal_by_user)

    # FIXME: Make the count happen in the DB
    for provider in providers:
        for signal in signals:
            if provider.id == signal.provider.id and signal.complete:
                provider.associated_signal = True

                if hasattr(provider, 'assoc_count'):
                    provider.assoc_count += 1
                else:
                    provider.assoc_count = 1

    return render(request, 'core/signals/providers.html', {
        'title': 'Ografy - Providers',
        'body_class': 'full',
        'providers': providers
    })


@login_required
def verify(request, pk):
    if request.method == 'GET':
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=pk)).get()
        endpoints = EndpointApi.get(Q(provider=signal.provider.id))
        permissions = PermissionApi.get(Q(signal=signal.id))
        initial_verification = False
        endpoint_list = {}

        for endpoint in endpoints:
            matched_auth_endpoint = False

            for permission in permissions:
                if permission.endpoint.id == endpoint.id:
                    matched_auth_endpoint = True
                    endpoint_list[endpoint] = permission

            if not matched_auth_endpoint:
                endpoint_list[endpoint] = None

        if signal.connected is False:
            return render(request, 'core/signals/authorize.html', {
                'title': 'Ografy - Authorize ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'current': 'verify',
                'signal': signal
            })
        else:
            if not signal.complete:
                initial_verification = True
                extra_data = UserSocialAuth.objects.filter(user=request.user.id, id=signal.usa_id)[0].extra_data

                if signal.provider.auth_type == 1:
                    access_token = extra_data['access_token']
                    signal.oauth_token = access_token['oauth_token']
                    signal.oauth_token_secret = access_token['oauth_token_secret']
                elif signal.provider.auth_type == 0:
                    signal.access_token = extra_data['access_token']

                signal.save()

            return render(request, 'core/signals/verify.html', {
                'title': 'Ografy - Verify ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal,
                'provider': signal.provider,
                'initial_verification': initial_verification,
                'current': 'verify',
                'endpoint_list': endpoint_list
            })
    elif request.method == 'POST':
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=pk)).get()

        if (not signal.complete):
            signal.complete = True
            signal.enabled = True

        user_social_auth_instance = UserSocialAuth.objects.filter(id=signal.usa_id).get()
        signal.name = request.POST['name']
        signal.frequency = int(request.POST['updateFrequency'])
        extra_data = user_social_auth_instance.extra_data

        # OAuth1 returns tokens on extra_data.  Signal.extra_data is serialized and sent to the user, and we don't
        # want those tokens available on the client, so delete them from signal.extra_data
        if 'access_token' in extra_data:
            if 'oauth_token' in extra_data['access_token']:
                extra_data['access_token'].pop('oauth_token')
                extra_data['access_token'].pop('oauth_token_secret')
            else:
                extra_data.pop('access_token')

        signal.extra_data = extra_data
        signal.save()

        # This handles updating the Permissions enabled status and the creation of Permissions.
        # The client passes a dictionary of Endpoint Definitions and their associated Permissions to the server.
        # The dictionary keys are the IDs of the Endpoint Definitions associated with this signal.
        # The dictionary values are either 'None' if an Permission has not been created for that endpoint
        # definition yet, or a dictionary if there is an Permission.
        # The sub-dictionary's key is the ID of the Permission, and the value is a boolean representing
        # whether or not the Permission is enabled.
        # Example:
        # {
        #   38920743: None,
        #   32957207: {
        #       38828502: False
        #   }
        # }
        # Endpoint definition 38920743 has no Permission associated with it.
        # Endpoint definition 32957207 has Permission 38828502 associated with it.
        # Permission 38828502 should be disabled.
        #

        # Get the endpoint dictionary from the request
        endpoints_dict = json.loads(request.POST['endpointsDict'])
        for index in endpoints_dict:
            # Get the Permission dictionary for this Endpoint Definition (or None if there is no Permission).
            this_endpoint_dict = endpoints_dict[index]
            # Get the Permission ID (or None if it doesn't exist)
            this_permission_id = list(this_endpoint_dict.keys())[0]

            # If the Permission exists, update its enabled status based on what was passed to the server
            if not this_permission_id == 'None':
                PermissionApi.patch(this_permission_id, {
                    'enabled': this_endpoint_dict[this_permission_id]
                })
            else:
                # If the Permission does not exist and the user wants that endpoint to be used, create an Permission.
                if this_endpoint_dict[this_permission_id]:
                    this_endpoint = EndpointApi.get(Q(id=index)).get()
                    url_parts = [''] * 6
                    url_parts[0] = this_endpoint.provider.scheme
                    url_parts[1] = this_endpoint.provider.domain
                    url_parts[2] = this_endpoint.path

                    if this_endpoint.provider.backend_name == 'facebook':
                        url_parts[3] = signal.usa_id
                        # This was the old way of joining, leaving in for reference until this is locked
                        # route = os.path.join(os.path.join(this_endpoint.provider.base_route, signal.usa_id, this_endpoint.path))

                    route = urllib.parse.urlunparse(url_parts)

                    new_permission = Permission(
                        name=this_endpoint.name,
                        route=route,
                        provider=this_endpoint.provider,
                        user_id=request.user.id,
                        signal=signal,
                        endpoint=this_endpoint,
                        enabled=True
                    )
                    PermissionApi.post(new_permission)

        return HttpResponse(reverse('core_providers'))
