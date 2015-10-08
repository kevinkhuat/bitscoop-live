from ografy.apps.passthrough.api.handler import (
    AccountHandler, EstimateLocationHandler, EventHandler, LocationHandler, SignalHandler
)
from ografy.apps.passthrough.proxy.handler import ExternalAPICall, Proxy, Signature


patterns = (
    (r'/call', ExternalAPICall),
    (r'/proxy', Proxy),
    (r'/signature', Signature),
    (r'/events', EventHandler),
    (r'/locations', LocationHandler),
    (r'/estimate', EstimateLocationHandler),
    (r'/signals', SignalHandler),
    (r'/account', AccountHandler)
)
