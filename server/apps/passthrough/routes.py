from server.apps.passthrough.api.handler import AccountHandler, EstimateLocationHandler, EventHandler, LocationHandler, ConnectionHandler
# from server.apps.passthrough.proxy.handler import ExternalAPICall, Proxy, Preview, Signature


patterns = (
    # (r'/call', ExternalAPICall),
    # (r'/proxy', Proxy),
    # (r'/signature', Signature),
    (r'/events', EventHandler),
    (r'/locations', LocationHandler),
    (r'/estimate', EstimateLocationHandler),
    (r'/connections', ConnectionHandler),
    (r'/account', AccountHandler)
)
