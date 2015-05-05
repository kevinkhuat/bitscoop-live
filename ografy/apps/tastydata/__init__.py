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


def parse_query(query_params, expression_class, **kwargs):
    query_filter = expression_class()

    if 'filter' in query_params:
        query = query_params['filter']
        # add filter query
        if 'filter' in query_params:
            query = query_params['filter']
            # add filter query
            query_filter = query_filter & parse_filter(query, expression_class=expression_class)
        if 'search' in query_params:
            search = query_params['search']
            # add search query
            query_filter = query_filter & expression_class
        if 'set' in query_params:
            set = query_params['set']

            query_filter = query_filter & expression_class().in_bulk(set)
        if 'exclude' in query_params:
            exclude = query_params['exclude']

            query_filter = query_filter & expression_class().where('id is NOT exclude')

    return query_filter


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
