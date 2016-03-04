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
from server.contrib.pytoolbox import initialize_endpoint_data
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

            usa_object = UserSocialAuth.objects.filter(user=user.id, id=connection.usa_id).get()
            metadata = usa_object.extra_data

            # Check for and remove any connections for the user with the same provider account.
            duplicate_connections = ConnectionApi.get(val=Q(user_id=user.id) & Q(provider_uid=usa_object.uid))

            if len(list(duplicate_connections)) > 0:
                connection.delete()
                usa_object.delete()

                return redirect_by_name('providers')

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
            if usa_object.uid is not '':
                connection.provider_uid = usa_object.uid

            connection.auth_status['complete'] = True
            connection.enabled = True

            connection.save()

            # Delete the PSA object to clear the process
            usa_object.delete()

            return redirect_by_name('providers')


class ConnectView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, name):
        expression = Q(name__iexact=name)
        provider = ProviderApi.get(expression).get()
        sources = provider.sources

        connection_by_user = Q(user_id=request.user.id)
        connections = ConnectionApi.get(val=connection_by_user)

        next_name_count = 1

        # FIXME: Make the count happen in the DB
        for connection in connections:
            if provider.provider_number == connection.provider.provider_number:
                next_name_count += 1

        return render(request, 'connections/connect.html', {
            'next_name_count': next_name_count,
            'current_count': next_name_count - 1,
            'title': 'BitScoop - Connect to ' + provider.name,
            'flex_override': True,
            'provider': provider,
            'source_dict': sources,
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

        # Get the source dictionary from the request
        permissions_list = json.loads(request.POST['permissions'])
        sources = provider.sources

        for source_name in permissions_list:
            for source in sources:
                if source == source_name:
                    new_permission = Permission(
                        enabled=True,
                        frequency=1
                    )
                    connection.permissions[source_name] = new_permission
                    connection.endpoint_data[source_name] = {}

                    initialize_endpoint_data(provider, connection, source, provider['sources'][source]['mapping'], provider['sources'][source]['population'])

        ConnectionApi.post(connection)

        return HttpResponse(reverse('social:begin', kwargs={'backend': provider.psa_legacy['backend_name']}))
