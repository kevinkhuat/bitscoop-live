import datetime
import json

from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from mongoengine import Q
from social.apps.django_app.default.models import UserSocialAuth

from ografy.contrib.multiauth.decorators import login_required
from ografy.core.api import ProviderApi, SignalApi
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

        user_signals = list(SignalApi.get(val=Q(user_id=request.user.id)))

        for backend in unassociated_backends:
            found = False

            for signal in user_signals:
                if signal.usa_id == backend.id:
                    found = True

            if not found:
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
            if provider.provider_number == signal.provider.provider_number and signal.complete:
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
        event_sources = ProviderApi.get(Q(provider_number=signal.provider.provider_number)).get().event_sources

        # If something went wrong with authorization,
        if signal.connected is False:
            return render(request, 'core/signals/authorize.html', {
                'title': 'Ografy - Authorize ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'current': 'verify',
                'signal': signal
            })
        else:
            signal_data = UserSocialAuth.objects.filter(user=request.user.id, id=signal.usa_id).get().extra_data
            # OAuth1 returns tokens on extra_data.  Signal.signal_data is serialized and sent to the user, and we don't
            # want those tokens available on the client, so delete them from signal.signal_data
            if signal.provider.auth_type == 1:
                signal.oauth_token = signal_data['access_token'].pop('oauth_token')
                signal.oauth_token_secret = signal_data['access_token'].pop('oauth_token_secret')
            elif signal.provider.auth_type == 0:
                signal.access_token = signal_data.pop('access_token')

                if hasattr(signal_data, 'refresh_token'):
                    signal.refresh_token = signal_data.pop('refresh_token')

            signal.signal_data = signal_data
            signal.save()

            return render(request, 'core/signals/verify.html', {
                'title': 'Ografy - Verify ' + signal.provider.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal,
                'provider': signal.provider,
                'current': 'verify',
                'event_source_dict': event_sources
            })
    elif request.method == 'POST':
        signal = SignalApi.get(Q(user_id=request.user.id) & Q(id=pk)).get()
        provider = ProviderApi.get(Q(provider_number=signal.provider.provider_number)).get()

        if not signal.complete:
            signal.complete = True
            signal.enabled = True

        signal.name = request.POST['name']
        signal.frequency = int(request.POST['updateFrequency'])
        signal.save()

        # Get the event_source dictionary from the request
        permissions_list = json.loads(request.POST['permissions'])
        event_sources = provider.event_sources

        for event_source_name in permissions_list:
            for event_source in event_sources:
                if event_source == event_source_name:
                    new_permission = Permission(
                        event_source=event_sources[event_source],
                        enabled=True
                    )
                    signal.permissions[event_source_name] = new_permission
                    signal.endpoint_data[event_source_name] = {}

                    for endpoint in event_sources[event_source]['endpoints']:
                        signal.endpoint_data[event_source_name][endpoint] = {}
                        parameter_descriptions = signal.permissions[event_source_name]['event_source']['endpoints'][endpoint]['parameter_descriptions']

                        for parameter in signal.permissions[event_source_name]['event_source']['endpoints'][endpoint]['parameter_descriptions']:
                            if 'default' in parameter_descriptions[parameter].keys():
                                if parameter_descriptions[parameter]['default'] == 'date_now':
                                    signal.endpoint_data[event_source_name][endpoint][parameter] = datetime.date.today().isoformat().replace('-', '/')
                                else:
                                    signal.endpoint_data[event_source_name][endpoint][parameter] = parameter_descriptions[parameter]['default']

        signal.save()

        return HttpResponse(reverse('core_providers'))
