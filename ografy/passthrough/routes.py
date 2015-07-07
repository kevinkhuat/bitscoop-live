from ografy.passthrough.proxy.handler import ExternalAPICall, Proxy, Signature
from ografy.passthrough.search.handler import DSLSearch, StructuredSearch, TextSearch


patterns = (
    (r'/call', ExternalAPICall),
    (r'/proxy', Proxy),
    (r'/signature', Signature),
    (r'/search/dsl/(.*)', DSLSearch),
    (r'/search/structured/(.*)', StructuredSearch),
    (r'/search/text/(.*)', TextSearch),
)
