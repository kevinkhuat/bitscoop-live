from __future__ import unicode_literals

from tastypie.exceptions import InvalidFilterError
import six

from tastydata.filters.expressions import tokenize, Symbol


def parse(string, inst):
    tokens = tokenize(string, inst)
    # We want this as a dictionary so we can pass it around by reference.
    lookup = {
        'token': six.next(tokens)
    }

    def match(comp=None):
        if comp and comp != lookup['token']:
            raise SyntaxError('Expected `{0}`'.format(comp.value))

        lookup['token'] = six.next(tokens)

    def expression(rbp=0):
        token = lookup['token']
        lookup['token'] = six.next(tokens)
        lhs = token.nud(expr=expression, match=match)

        while rbp < lookup['token'].lbp:
            token = lookup['token']
            lookup['token'] = six.next(tokens)
            lhs = token.led(lhs=lhs, expr=expression)

        return lhs

    result = expression()

    if lookup['token'] != Symbol.get('(end)'):
        raise InvalidFilterError('Invalid token: `{0}`'.format(lookup['token'].value))

    return result