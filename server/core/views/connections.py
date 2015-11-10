import datetime
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from mongoengine import Q
from social.apps.django_app.default.models import UserSocialAuth

from server.contrib.multiauth.decorators import login_required
from server.contrib.pytoolbox.django.response import redirect_by_name
from server.core.api import ProviderApi, SignalApi
from server.core.documents import Permission, Signal


class AuthorizeView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        unassociated_backends = list(UserSocialAuth.objects.filter(user=user))
        unverified_signals = list(SignalApi.get(val=Q(user_id=user.id) & (Q(complete=False) | Q(connected=False))))
        signal_count = len(unverified_signals)

        # If there is more than one unverified+incomplete signal,
        # delete all and start over.
        if signal_count == 0 or signal_count > 1:
            # TODO: Change to bulk delete
            for signal in unverified_signals:
                SignalApi.delete(val=signal.id)

            user_signals = list(SignalApi.get(val=Q(user_id=user.id)))

            for backend in unassociated_backends:
                found = False

                for signal in user_signals:
                    if signal.usa_id == backend.id:
                        found = True

                if not found:
                    UserSocialAuth.objects.get(id=backend.id).delete()

            return redirect_by_name('providers')
        else:
            signal = unverified_signals[0]

            signal_data = UserSocialAuth.objects.filter(user=user.id, id=signal.usa_id).get().extra_data

            # OAuth1 returns tokens on extra_data.  Signal.signal_data is serialized and sent to the user, and we don't
            # want those tokens available on the client, so delete them from signal.signal_data
            if signal.provider.auth_type == 1:
                signal.oauth_token = signal_data['access_token'].pop('oauth_token')
                signal.oauth_token_secret = signal_data['access_token'].pop('oauth_token_secret')
            # OAuth2 also returns tokens on extra_data, and we similarly do not want those tokens passed to the client.
            elif signal.provider.auth_type == 0:
                signal.access_token = signal_data.pop('access_token')

                if 'refresh_token' in signal_data.keys():
                    signal.refresh_token = signal_data.pop('refresh_token')

            signal.signal_data = signal_data
            signal.complete = True
            signal.enabled = True

            signal.save()

            return redirect_by_name('providers')


class ConnectView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, name):
        expression = Q(name__iexact=name)
        provider = ProviderApi.get(expression).get()
        event_sources = provider.event_sources

        return render(request, 'core/connections/connect.html', {
            'title': 'BitScoop - Connect to ' + provider.name,
            'flex_override': True,
            'provider': provider,
            'event_source_dict': event_sources,
            'postback_url': reverse('connections:authorize')
        })

    def post(self, request, name):
        expression = Q(name__iexact=name)
        provider = ProviderApi.get(expression).get()

        signal = Signal(
            user_id=request.user.id,
            frequency=int(request.POST['updateFrequency']),
            provider=provider,
            name=request.POST['name'],
            connected=True,
            complete=False,
            enabled=False,
            created=datetime.datetime.now(),
            updated=datetime.datetime.now(),
            last_run=None
        )

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

        SignalApi.post(signal)

        return HttpResponse(reverse('social:begin', kwargs={'backend': provider.backend_name}))
