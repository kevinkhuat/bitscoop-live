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
from server.core.api import ConnectionApi, ProviderApi
from server.core.documents import Connection, Permission


class AuthorizeView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        unassociated_backends = list(UserSocialAuth.objects.filter(user=user))
        unverified_connections = list(ConnectionApi.get(val=Q(user_id=user.id) & (Q(auth_status__complete=False) | Q(auth_status__connected=False))))
        connection_count = len(unverified_connections)

        # If there is more than one unverified+incomplete connection,
        # delete all and start over.
        if connection_count == 0 or connection_count > 1:
            # TODO: Change to bulk delete
            for connection in unverified_connections:
                ConnectionApi.delete(val=connection.id)

            user_connections = list(ConnectionApi.get(val=Q(user_id=user.id)))

            for backend in unassociated_backends:
                found = False

                for connection in user_connections:
                    if connection.usa_id == backend.id:
                        found = True

                if not found:
                    UserSocialAuth.objects.get(id=backend.id).delete()

            return redirect_by_name('providers')
        else:
            connection = unverified_connections[0]

            metadata = UserSocialAuth.objects.filter(user=user.id, id=connection.usa_id).get().extra_data

            # OAuth1 returns tokens on extra_data.  Connection.connection_data is serialized and sent to the user, and we don't
            # want those tokens available on the client, so delete them from connection.connection_data
            if connection.provider.auth_type == 1:
                connection.auth_data['oauth_token'] = metadata['access_token'].pop('oauth_token')
                connection.auth_data['oauth_token_secret'] = metadata['access_token'].pop('oauth_token_secret')
            # OAuth2 also returns tokens on extra_data, and we similarly do not want those tokens passed to the client.
            elif connection.provider.auth_type == 0:
                connection.auth_data['access_token'] = metadata.pop('access_token')

                if 'refresh_token' in metadata.keys():
                    connection.auth_data['refresh_token'] = metadata.pop('refresh_token')

            connection.metadata = metadata
            connection.auth_status['complete'] = True
            connection.enabled = True

            connection.save()

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
        auth_status = {
            'connected': True,
            'complete': False
        }

        connection = Connection(
            auth_status=auth_status,
            user_id=request.user.id,
            frequency=int(request.POST['updateFrequency']),
            provider=provider,
            name=request.POST['name'],
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
                        enabled=True,
                        frequency=1
                    )
                    connection.permissions[event_source_name] = new_permission
                    connection.endpoint_data[event_source_name] = {}

                    for endpoint in event_sources[event_source]['endpoints']:
                        connection.endpoint_data[event_source_name][endpoint] = {}
                        parameter_descriptions = provider['endpoints'][endpoint]['parameter_descriptions']

                        for parameter in provider['endpoints'][endpoint]['parameter_descriptions']:
                            if 'default' in parameter_descriptions[parameter].keys():
                                if parameter_descriptions[parameter]['default'] == 'date_now':
                                    connection.endpoint_data[event_source_name][endpoint][parameter] = datetime.date.today().isoformat().replace('-', '/')
                                else:
                                    connection.endpoint_data[event_source_name][endpoint][parameter] = parameter_descriptions[parameter]['default']

        ConnectionApi.post(connection)

        return HttpResponse(reverse('social:begin', kwargs={'backend': provider.backend_name}))
