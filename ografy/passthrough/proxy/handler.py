import json

import tornado.web
from bson.objectid import ObjectId
from motorengine import Q
from tornado import gen

from ografy.passthrough.auth import user_authenticated
from ografy.passthrough.documents import AuthorizedEndpoint
from ografy.passthrough.proxy import psa_adapters


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
        This handles the process of getting the full Authorized Endpoint from the ID that's passed in as an argument on the request,
        getting the route and signal from the endpoint, getting the PSA backend definitions, adding any OAuth or OpenID tokens/keys
        that couldn't be sent from the client, then calling the route in question and returning the results to the client.

        :param user:
        :return:
        """
        # Need to cast the ObjectID as such since MotorEngine doesn't handle the raw string well
        authorized_endpoint_id = ObjectId(self.get_argument('authorized_endpoint_id'))
        # Query based on the ID and user ID for extra security
        authorized_endpoint_query = Q({'_id': authorized_endpoint_id}) & Q(user_id=self.request.user.id)
        # Get the Authorized Endpoint; as the result is a list, pluck the 0th element from the result
        authorized_endpoint_list = yield AuthorizedEndpoint.objects.filter(authorized_endpoint_query).find_all()
        authorized_endpoint = authorized_endpoint_list[0]

        # Get the route from the endpoint
        route = authorized_endpoint.route
        # Need to explicitly load the Authorized Endpoint's reference to its associated field
        yield authorized_endpoint.load_references(fields=['signal'])
        # Get the signal from the endpoint, and load the reference to its provider
        signal = authorized_endpoint.signal
        yield signal.load_references(fields=['provider'])

        # 'Fun' PSA code for getting the backend associated with the signal
        backend_module = psa_adapters.get_backend_module(signal)
        loaded_backend = psa_adapters.get_psa_backend(signal)

        # Get the parameters from the request, then populate the ones that couldn't be sent by the client,
        # such as OAuth tokens and OpenID keys.
        parameters = json.loads(self.get_argument('parameters'))
        parameters = psa_adapters.add_psa_params(parameters, signal)

        # TODO: Replace OAuth1 authorization with something other than PSA
        # For now, we're using PSA's authorization for OAuth1 since it was going to be a pain to write
        # our own implementation.  Although Tornado's Auth might not be so bad.
        # This is somewhat synchronous, but it'll be fine for initial testing
        if hasattr(backend_module, 'BaseOAuth1'):
            response = loaded_backend.get_json(
                route,
                auth=loaded_backend.oauth_auth(parameters)
            )
            self.write(json.dumps(response))
            self.finish()
        # If it's not OAuth1, call psa_get_json to add the parameters to the URL and call it, then send the results to the client.
        else:
            psa_adapters.psa_get_json(self, route, parameters, loaded_backend)

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
            authorized_endpoint_id = ObjectId(self.get_argument('authorized_endpoint_id'))
            authorized_endpoint_query = Q({'_id': authorized_endpoint_id}) & Q(user_id=self.request.user.id)
            authorized_endpoint_list = yield AuthorizedEndpoint.objects.filter(authorized_endpoint_query).find_all()
            authorized_endpoint = authorized_endpoint_list[0]
            route = authorized_endpoint.route

            parameters = json.loads(self.get_argument('parameters'))

            request = tornado.httpclient.HTTPRequest(route, **parameters)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield client.fetch(request)
            self.write(response.body)
            self.finish()

        except Exception:
            self.send_error()
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
            authorized_endpoint_id = ObjectId(self.get_argument('authorized_endpoint_id'))
            authorized_endpoint_query = Q({'_id': authorized_endpoint_id}) & Q(user_id=self.request.user.id)
            authorized_endpoint_list = yield AuthorizedEndpoint.objects.filter(authorized_endpoint_query).find_all()
            authorized_endpoint = authorized_endpoint_list[0]

            yield authorized_endpoint.load_references(fields=['signal'])
            signal = authorized_endpoint.signal
            yield signal.load_references(fields=['provider'])

            parameters = {'pauth'}
            parameters = psa_adapters.add_psa_params(parameters, signal)

            self.write(parameters)
            self.finish()

        except Exception:
            self.send_error()
            self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()
