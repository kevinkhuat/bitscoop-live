from ografy.passthrough.proxy.handler import ExternalAPICall, Proxy, Signature
from ografy.passthrough.search.handler import ESSearch


patterns = (
    (r'/call', ExternalAPICall),
    (r'/proxy', Proxy),
    (r'/signature', Signature),
    (r'/search', ESSearch),
)
