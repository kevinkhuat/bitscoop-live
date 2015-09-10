from ografy.apps.passthrough.proxy.handler import ExternalAPICall, Proxy, Signature
from ografy.apps.passthrough.search.handler import ESSearch


patterns = (
    (r'/call', ExternalAPICall),
    (r'/proxy', Proxy),
    (r'/signature', Signature),
    (r'/search', ESSearch),
)
