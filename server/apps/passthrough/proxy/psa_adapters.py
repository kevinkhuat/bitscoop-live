import json
import re
import urllib

import tornado.httpclient
import tornado.web
from django.conf import settings
from django.utils.module_loading import import_module
from social.backends.utils import get_backend
from social.exceptions import AuthFailed
from social.utils import SSLHttpAdapter, module_member, setting_name, user_agent
from tornado import gen


# This is ugly code ripped out of PSA that is needed right now to allow for calling social auths.
# It should be replaced at some point with something better.
BACKENDS = settings.AUTHENTICATION_BACKENDS

STORAGE = getattr(settings, setting_name('STORAGE'), 'social.apps.django_app.default.models.DjangoStorage')
Storage = module_member(STORAGE)

STRATEGY = getattr(settings, setting_name('STRATEGY'), 'social.strategies.django_strategy.DjangoStrategy')
Strategy = module_member(STRATEGY)

HEADER_REPLACEMENT = re.compile('\[\$1\]')


def refresh_connection_token(loaded_backend, connection):
    refresh_response = loaded_backend.refresh_token(connection.refresh_token)
    connection.auth_data.access_token = refresh_response['access_token']
    connection.save()
    return connection


def get_psa_backend(connection):
    """
    Return the PSA backend associated with a given connection

    :param connection:
    :return: the PSA backend for the given connection
    """
    redirect_uri = '/'
    backend_class = get_backend(BACKENDS, connection.provider.backend_name)

    return backend_class(Strategy(Storage), redirect_uri)


def get_backend_module(connection):
    """
    Return the backend module associated with a given connection

    :param connection:
    :return: the backend module for the given connection
    """
    name = format(connection.provider.name.lower())

    if name in ['reddit', 'slice', 'spotify']:
        return import_module('server.contrib.psafixbox.backends.' + name)
    else:
        return import_module('social.backends.' + name)


def hydrate_server_fields(items, connection):
    """
    This takes in a dictionary of items (parameters or headers) and their associated connection and populates any items that
    could not be populated on the client, specifically OAuth tokens and OpenID keys.
    This information is assumed to be stored somewhere on the connection.
    The items in question come in storing their location on the connection, e.g. the OAuth2 Access token
    comes in as {access_token: 'access_token'}, with the value of this key/value pair indicating that the
    information is located at connection.access_token.

    :param items: The dictionary of parameter names and values
    :param connection: The associated connection
    :return: A dictionary of the items for the given call
    """
    for item in items:
        if (item == 'oauth_token' or item == 'oauth_token_secret' or item == 'access_token' or item == 'key') and (items[item] == 'oauth_token' or items[item] == 'oauth_token_secret' or items[item] == 'access_token' or items[item] == 'key'):
            # Find the token location from the endpoint definition, currently assumes it's on the connection's explicitly populated property
            token_location = items[item].split('.')

            sliced = connection
            for index in token_location:
                sliced = sliced._values[index]

            items[item] = sliced

    return items


@gen.coroutine
def psa_get_json(self, url, parameters, headers, header_descriptions, pagination_method, connection, loaded_backend, method='GET', *args, **kwargs):
    """
    This appends the parameters to the URL call and then calls the URL asynchronously.
    When the result comes back, it is written back to the client.

    :param url: The URL to call
    :param parameters: The parameters to append to the call
    :param loaded_backend: The backend associated with call
    :param method: The method to use to make the call
    :param args:
    :param kwargs:
    :return:
    """
    kwargs.setdefault('headers', {})

    for header, value in headers.items():
        this_header_description = header_descriptions[header]

        header_value = re.sub(HEADER_REPLACEMENT, value, this_header_description['header_value'])
        kwargs['headers'][this_header_description['header_name']] = header_value

    # Add parameters to URL manually using urllib
    # kwargs.setdefault('params', parameters)
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(parameters)

    url_parts[4] = urllib.parse.urlencode(query)
    url = urllib.parse.urlunparse(url_parts)

    if loaded_backend.setting('VERIFY_SSL') is not None:
        kwargs.setdefault('verify', loaded_backend.setting('VERIFY_SSL'))
    kwargs.setdefault('connect_timeout', loaded_backend.setting('REQUESTS_TIMEOUT') or loaded_backend.setting('URLOPEN_TIMEOUT'))
    if loaded_backend.SEND_USER_AGENT and 'User-Agent' not in kwargs['headers']:
        kwargs['headers']['User-Agent'] = user_agent()

    try:
        if loaded_backend.SSL_PROTOCOL:
            # TODO: Replace with tornado equivalent of SSL and remove REQUESTS!
            session = SSLHttpAdapter.ssl_adapter_session(loaded_backend.SSL_PROTOCOL)
            response = session.request(method, url, *args, **kwargs)
            self.write(response)
            self.finish()
        else:
            if method == 'POST':
                kwargs['method'] = method
                kwargs['body'] = ''

            request = tornado.httpclient.HTTPRequest(url, **kwargs)
            client = tornado.httpclient.AsyncHTTPClient()

            try:
                response = yield client.fetch(request)

                if pagination_method == 'rfc5988' and 'Link' in response.headers:
                    constructed_response = {
                        'Link': response.headers['Link'],
                        'data': json.loads(response.body.decode('utf-8'))
                    }

                    constructed_response = json.dumps(constructed_response).encode('utf-8')
                else:
                    constructed_response = response.body

                self.write(constructed_response)
                self.finish()
            except tornado.httpclient.HTTPError as err:
                if err.response.code == 401:
                    connection = refresh_connection_token(loaded_backend, connection)

                    parameters['access_token'] = connection.auth_data.access_token

                    url_parts = list(urllib.parse.urlparse(url))
                    query = dict(urllib.parse.parse_qsl(url_parts[4]))
                    query.update(parameters)

                    url_parts[4] = urllib.parse.urlencode(query)
                    url = urllib.parse.urlunparse(url_parts)

                    request = tornado.httpclient.HTTPRequest(url, **kwargs)
                    client = tornado.httpclient.AsyncHTTPClient()
                    try:
                        response = yield client.fetch(request)

                        if pagination_method == 'rfc5988' and 'Link' in response.headers:
                            constructed_response = {
                                'Link': response.headers['Link'],
                                'data': json.loads(response.body.decode('utf-8'))
                            }

                            constructed_response = json.dumps(constructed_response).encode('utf-8')
                        else:
                            constructed_response = response.body

                        self.write(constructed_response)
                        self.write(err)
                    except tornado.httpclient.HTTPError as err:
                        if err.code in [401, 404, 429]:
                            self.write({
                                'error': err.code
                            })
                            self.finish()
                        else:
                            self.send_error(err.code)
                else:
                    if err.code in [401, 404, 429]:
                        self.write({
                            'error': err.code
                        })
                        self.finish()
                    else:
                        self.send_error(err.code)
    except ConnectionError as err:
        raise AuthFailed(loaded_backend, str(err))
