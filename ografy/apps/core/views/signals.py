import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from social.apps.django_app.default.models import UserSocialAuth

from ografy.apps.core import api as core_api


@login_required
def authorize(request):

    # # Look up signals from API for current user where signal
    # # is not verified or complete.
    unassociated_backends = list(UserSocialAuth.objects.filter(user=request.user))
    unverified_signals = list(core_api.SignalApi.get(val=Q(user=request.user.id) & (Q(complete=False) | Q(connected=False))))

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
            core_api.SignalApi.delete(val=signal.id)

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
    provider = core_api.ProviderApi.get(Q(id=pk)).get()

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
    provider = core_api.ProviderApi.get(Q(backend_name=name)).get()

    return HttpResponseRedirect(reverse('core_connect', kwargs={'pk': provider.id}))

@login_required
def providers(request):
    providers = list(core_api.ProviderApi.get())
    signal_by_user = Q(user_id=request.user.id)
    signals = core_api.SignalApi.get(val=signal_by_user)
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
        signal = core_api.SignalApi.get(Q(user=request.user.id) & Q(id=pk)).get()
        permissions = signal.permission_set.all()

        if signal.connected is False:
            return render(request, 'core/signals/authorize.html', {
                'title': 'Ografy - Authorize ' + signal.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal
            })
        else:
            extra_data = UserSocialAuth.objects.filter(user=request.user, uid=signal.psa_backend_uid)[0].extra_data;
            if 'access_token' in extra_data:
                access_token = extra_data['access_token']
                if 'oauth_token' in access_token:
                    signal.oauth_token = access_token['oauth_token']
                    signal.oauth_token_secret = access_token['oauth_token_secret']
                else:
                    signal.access_token = access_token
            signal.save()

            return render(request, 'core/signals/verify.html', {
                'title': 'Ografy - Verify ' + signal.name + ' Connection',  # Change to signal
                'flex_override': True,
                'content_class': 'left',
                'signal': signal,
                'permissions': permissions
            })
    elif request.method == 'POST':
        signal = core_api.SignalApi.get(Q(user=request.user.id) & Q(id=pk)).get()
        signal.complete = True
        signal.enabled = True
        signal.frequency = request.POST['updateFrequency']
        signal.save()

        requestPermissions = json.loads(request.POST['permissions'])
        permissions = signal.permission_set.all()
        for count in range(0, len(permissions)):
            permissions[count].enabled = requestPermissions[count]
            permissions[count].save()

        return HttpResponse(json.dumps(reverse('core_settings_signals')))
