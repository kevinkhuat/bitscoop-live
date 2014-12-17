from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect

from social.apps.django_app.default.models import UserSocialAuth

from ografy.apps.core import api as core_api


def authorize(request, pk=None):
    # Look up signals from API for current user where signal
    # is not verified or complete.
    connected_backends = UserSocialAuth.objects.get(user=request.user)
    unverified_signals = core_api.SignalApi.get(val=Q(user=request.user.id) | Q(verified=False)).get()

    unassociated_backends = connected_backends
    backend_uid = None

    # If there is more than one unverified+incomplete signal,
    # delete all but the newest one.
    for signal in unverified_signals:
        for backend in connected_backends:
            if backend.uid == signal.psa_backend_uid:
                unassociated_backends.remove(backend)

    # Messed up backend
    if len(unassociated_backends) == 0:
        # TODO: Change to bulk delete
        if len(unverified_signals) > 0:
            for signal in unverified_signals:
                core_api.SignalApi.delete(val=signal.id)
        HttpResponseRedirect(reverse('core_providers'))
    elif len(unassociated_backends) > 1:
        for backend in unassociated_backends:
            UserSocialAuth.objects.get(uid=backend.uid).delete()
        HttpResponseRedirect(reverse('core_providers'))
    else:
        backend_uid = unassociated_backends[0].uid

    # Messed up signals
    if len(unverified_signals) == 0:
        # TODO: Change to bulk delete
        if len(unassociated_backends) > 0:
            for backend in unassociated_backends:
                UserSocialAuth.objects.get(uid=backend.uid)
        HttpResponseRedirect(reverse('core_providers'))

    if pk is None:
        HttpResponseRedirect(reverse('core_providers'))
    else:
        signal = unverified_signals.get(val=Q(id=pk)).get()
        if signal is None:
            HttpResponseRedirect(reverse('core_providers'))

        signal.psa_backend_uid = backend_uid
        signal.verified = True

    return render(request, 'core/signals/authorize.html', {
        'title': 'Ografy - Authorize ' + signal.name + ' Connection',
        'content_class': 'left',
        'signal': signal
    })


def connect(request, pk):
    provider = core_api.ProviderApi.get(Q(id=pk)).get()

    return render(request, 'core/signals/connect.html', {
        'title': 'Ografy - Connect to ' + provider.name,
        'content_class': 'left',
        'provider': provider,
        'user_id': request.user.id,
        'postback_url': reverse('core_authorize')
    })


def connect_name(request, name):
    provider = core_api.ProviderApi.get(Q(backend_name=name)).get()

    return HttpResponseRedirect(reverse('core_connect', kwargs={'pk': provider.id}))


def providers(request):
    providers = core_api.ProviderApi.get()
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
        'content_class': 'bordered left',
        'providers': providers,
        'connect_url': connect_url
    })


def verify(request, pk):
    signal = core_api.SignalApi.get(Q(id=pk)).get()

    return render(request, 'core/signals/verify.html', {
        'title': 'Ografy - Verify ' + signal.name + ' Connection',
        'content_class': 'left',
        'signal': signal
    })
