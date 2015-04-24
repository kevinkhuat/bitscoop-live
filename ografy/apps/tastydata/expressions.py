import re
import types
import json

from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from ografy.apps.tastydata.exceptions import InvalidFilterError


TOKEN_SPLIT = re.compile("((?:[0-9]+\.[0-9]*)|(?:[0-9]*\.[0-9]+)|\w+|\(|\)|(?:'[^\']*'))")
COMPARERS = {
    'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith',
    'exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull',
    'regex', 'iregex', 'geo_within_polygon', 'near', 'max_distance'
}


class Symbol(object):
    _cache = {}

    @classmethod
    def register(cls, value, *args, **kwargs):
        symbol = cls(value, *args, **kwargs)
        Symbol._cache[value] = symbol

    @classmethod
    def get(cls, value, *args, **kwargs):
        if value in Symbol._cache:
            return Symbol._cache[value]
        else:
            return cls(value, *args, **kwargs)

    def __init__(self, value, lbp=0):
        self.id = value
        self.value = value
        self.lbp = lbp

    def nud(self, *args, **kwargs):
        raise Exception('Undefined.')

    def led(self):
        raise Exception('Missing operator.')

    def __str__(self, *args, **kwargs):
        if self.id == self.value:
            return '<{0}: {1} -> {2}>'.format(self.__class__.__name__, self.id, self.lbp)
        else:
            return '<{0}: {1}={2} -> {3}>'.format(self.__class__.__name__, self.id, self.value, self.lbp)


class Predicate(Symbol):
    def __init__(self, field, operator, literal, expression_class=Q):
        super(Predicate, self).__init__(field, lbp=0)
        self.field = field
        self.operator = operator
        self.literal = literal
        self.expression_class = expression_class

    def nud(self, *args, **kwargs):
        lhs = '{0}{1}{2}'.format(self.field, LOOKUP_SEP, self.operator)

        return self.expression_class(**{
            lhs: self.literal
        })


class Infix(Symbol):
    def __init__(self, value, lbp=0, led=None):
        super(Infix, self).__init__(value, lbp)

        if callable(led):
            self.led = types.MethodType(led, self)


class Prefix(Symbol):
    def __init__(self, value, lbp=70, nud=None):
        super(Prefix, self).__init__(value, lbp)

        if callable(nud):
            self.nud = types.MethodType(nud, self)


def _get_literal_value(value, operator):
    if value == 'True' or value == 'true':
        return True
    elif value == 'False' or value == 'false':
        return False
    elif value[0] == '\'' and value[-1] == '\'':
        if operator == 'geo_within_polygon' or operator == 'near':
            return json.loads(value[1:-1])
        else:
            return value[1:-1]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def _and_led(self, lhs, expr, **kwargs):
    return lhs & expr(self.lbp)


def _lparen_nud(self, expr, match, **kwargs):
    value = expr()
    match(Symbol.get(')'))

    return value


def _not_nud(self, expr, **kwargs):
    return ~expr(self.lbp)


def _or_led(self, lhs, expr, **kwargs):
    return lhs | expr(self.lbp)


def tokenize(string, expression_class=Q):
    tokens = TOKEN_SPLIT.findall(string)

    while len(tokens) > 0:
        token = tokens.pop(0)

        if token in Symbol._cache:
            yield Symbol._cache[token]
        else:
            field = token

            try:
                operator = tokens.pop(0)
                raw_literal = tokens.pop(0)
            except IndexError:
                raise InvalidFilterError('Incomplete predicate format at: `{0}`'.format(field))

            if operator not in COMPARERS:
                raise InvalidFilterError('Unexpected filter function: `{0}`'.format(operator))

            literal = _get_literal_value(raw_literal, operator)

            yield Predicate(field, operator, literal, expression_class=expression_class)

    yield Symbol.get('(end)')


if __name__:
    Symbol.register('(end)')
    Infix.register('or', 50, led=_or_led)
    Infix.register('and', 60, led=_and_led)
    Prefix.register('not', nud=_not_nud)
    Prefix.register('(', 0, nud=_lparen_nud)
    Prefix.register(')', 0)
