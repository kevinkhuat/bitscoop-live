import json
import re
import urllib

import tornado.web
from bson.objectid import ObjectId
from motorengine import Q
from tornado import gen

from server.apps.passthrough.auth import user_authenticated
from server.apps.passthrough.documents import Signal
from server.apps.passthrough.proxy import psa_adapters


# Handlers that are used for calling provider endpoints
# Note that each type needs the 'options' function defined so that cross-domain requests can be made properly.
# The reason that there isn't any code in them other than self.finish() is that all of the headers that need
# to be set for CORS are done so by Nginx.
class ExternalAPICall(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self):
        """
        This handles the process of getting the full Endpoint from the ID that's passed in as an argument on the request,
        getting the route and signal from the endpoint, getting the PSA backend definitions, adding any OAuth or OpenID tokens/keys
        that couldn't be sent from the client, then calling the route in question and returning the results to the client.

        :param user:
        :return:
        """
        # Need to cast the ObjectID as such since MotorEngine doesn't handle the raw string well
        endpoint_name = self.get_argument('endpoint_name')
        permission_name = self.get_argument('permission_name')
        signal_id = ObjectId(self.get_argument('signal_id'))
        signal_query = Q({'_id': signal_id})

        signal_list = yield Signal.objects.filter(signal_query).find_all()
        signal = signal_list[0]
        endpoint = signal.permissions[permission_name]['event_source']['endpoints'][endpoint_name]
        pagination_method = signal.permissions[permission_name]['event_source']['mappings']['pagination']['method']

        # Get the route from the endpoint
        route = endpoint['route']

        # Need to explicitly load the Signal's reference to its Provider
        yield signal.load_references(fields=['provider'])

        # 'Fun' PSA code for getting the backend associated with the signal
        backend_module = psa_adapters.get_backend_module(signal)
        loaded_backend = psa_adapters.get_psa_backend(signal)

        # Get the parameters from the request, then populate the ones that couldn't be sent by the client,
        # such as OAuth tokens and OpenID keys.
        parameters = json.loads(self.get_argument('parameters'))
        headers = json.loads(self.get_argument('headers'))
        header_descriptions = endpoint['header_descriptions']

        for additional_path_field in endpoint['additional_path_fields']:
            path_parameter = parameters.pop(additional_path_field['parameter'])

            if type(path_parameter) is int:
                path_parameter = str(path_parameter)

            route = re.sub(re.escape(additional_path_field['replace']), path_parameter, route)

        parameters = psa_adapters.hydrate_server_fields(parameters, signal)
        headers = psa_adapters.hydrate_server_fields(headers, signal)

        # TODO: Replace OAuth1 authorization with something other than PSA
        # For now, we're using PSA's authorization for OAuth1 since it was going to be a pain to write
        # our own implementation.  Although Tornado's Auth might not be so bad.
        # This is somewhat synchronous, but it'll be fine for initial testing
        if hasattr(backend_module, 'BaseOAuth1') and not hasattr(backend_module, 'BaseOAuth2'):
            non_oauth_parameters = {}

            for parameter in parameters:
                if parameter != 'oauth_token' and parameter != 'oauth_token_secret':
                    non_oauth_parameters[parameter] = parameters[parameter]

            url_parts = list(urllib.parse.urlparse(route))
            query = dict(urllib.parse.parse_qsl(url_parts[4]))
            query.update(non_oauth_parameters)

            url_parts[4] = urllib.parse.urlencode(query)
            route = urllib.parse.urlunparse(url_parts)

            response = loaded_backend.get_json(
                route,
                auth=loaded_backend.oauth_auth(parameters)
            )
            self.write(json.dumps(response))
            self.finish()
        # If it's not OAuth1, call psa_get_json to add the parameters to the URL and call it, then send the results to the client.
        else:
            psa_adapters.psa_get_json(self, route, parameters, headers, header_descriptions, pagination_method, signal, loaded_backend, method=endpoint['call_method'])

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class Proxy(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self):
        """This rest endpoint will make an API call on the server.

        #. *request* a request object must contain the variable:

            #. api_call_url

        * returns: returns the response from the call or an error.
        """
        try:
            # Get API URL
            endpoint_name = self.get_argument('endpoint_name')
            permission_name = self.get_argument('permission_name')
            signal_id = ObjectId(self.get_argument('signal_id'))
            signal_query = Q({'_id': signal_id})

            signal_list = yield Signal.objects.filter(signal_query).find_all()
            signal = signal_list[0]
            endpoint = signal.permissions[permission_name]['event_source']['endpoints'][endpoint_name]

            # Get the route from the endpoint
            route = endpoint['route']

            parameters = json.loads(self.get_argument('parameters'))

            request = tornado.httpclient.HTTPRequest(route, **parameters)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield client.fetch(request)
            self.write(response.body)
            self.finish()

        except Exception:
            self.send_error(Exception)
            self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class Signature(tornado.web.RequestHandler):
    # This signs a request with the proper tokens/keys but does not make the request,
    # instead just passing back the signing parameters.
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self):
        try:
            # TODO: Need to properly sign an OAuth1 call
            # TODO: requests handled this step synchronously with requests.OAuth1lib
            endpoint_name = self.get_argument('endpoint_name')
            permission_name = self.get_argument('permission_name')
            signal_id = ObjectId(self.get_argument('signal_id'))
            signal_query = Q({'_id': signal_id})

            signal_list = yield Signal.objects.filter(signal_query).find_all()
            signal = signal_list[0]
            endpoint = signal.permissions[permission_name]['event_source']['endpoints'][endpoint_name]

            # Get the route from the endpoint
            route = endpoint['route']

            # Need to explicitly load the Signal's reference to its Provider
            yield signal.load_references(fields=['provider'])

            # Get the parameters from the request, then populate the ones that couldn't be sent by the client,
            # such as OAuth tokens and OpenID keys.
            parameters = json.loads(self.get_argument('parameters'))
            for additional_path_field in endpoint['additional_path_fields']:
                path_parameter = parameters.pop(additional_path_field['parameter'])
                route = re.sub(re.escape(additional_path_field['replace']), path_parameter, route)

            parameters = psa_adapters.add_psa_params(parameters, signal)

            self.write(parameters)
            self.finish()

        except Exception:
            self.send_error()
            self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()
