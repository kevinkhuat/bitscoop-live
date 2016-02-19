from server.apps.passthrough.api.handler import (
    AccountHandler, ConnectionHandler, EstimateLocationHandler, EventHandler, LocationHandler, SearchesHandler,
    SearchesIDHandler, SearchHandler
)


# from server.apps.passthrough.proxy.handler import ExternalAPICall, Proxy, Preview, Signature


patterns = (
    # (r'/call', ExternalAPICall),
    # (r'/proxy', Proxy),
    # (r'/signature', Signature),
    (r'/events', EventHandler),
    (r'/search', SearchHandler),
    (r'/searches', SearchesHandler),
    (r'/searches/([\w-]+)', SearchesIDHandler),
    (r'/locations', LocationHandler),
    (r'/estimate', EstimateLocationHandler),
    (r'/connections', ConnectionHandler),
    (r'/account', AccountHandler)
)
