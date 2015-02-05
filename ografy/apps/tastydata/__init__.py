import urllib.parse as urlparse

from ografy.apps.tastydata.exceptions import InvalidFilterError
from ografy.apps.tastydata.expressions import tokenize, Symbol


CONTROL_PARAMS = {'filter', 'set', 'skip', 'top', 'search'}


def get_query_string(kwargs={}):
    params = []

    for key, value in kwargs.items():
        formatted_key = key if key in CONTROL_PARAMS else urlparse.quote(key)
        formatted_value = urlparse.quote(str(value))
        params.append('%s=%s' % (formatted_key, formatted_value))

    return '&'.join(params)


def parse_filter(string, **kwargs):
    tokens = tokenize(string, **kwargs)
    # We want this as a dictionary so we can pass it around by reference.
    lookup = {
        'token': next(tokens)
    }

    def match(comp=None):
        if comp and comp != lookup['token']:
            raise SyntaxError('Expected `{0}`'.format(comp.value))

        lookup['token'] = next(tokens)

    def expression(rbp=0):
        token = lookup['token']
        lookup['token'] = next(tokens)
        lhs = token.nud(expr=expression, match=match)

        while rbp < lookup['token'].lbp:
            token = lookup['token']
            lookup['token'] = next(tokens)
            lhs = token.led(lhs=lhs, expr=expression)

        return lhs

    result = expression()

    if lookup['token'] != Symbol.get('(end)'):
        raise InvalidFilterError('Invalid token: `{0}`'.format(lookup['token'].value))

    return result
