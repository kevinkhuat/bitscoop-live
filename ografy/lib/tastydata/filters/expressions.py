from __future__ import unicode_literals
import re
import types

from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from tastypie.exceptions import InvalidFilterError
import six

import tastydata.util as util


# OData Filter Spec
# http://www.odata.org/documentation/odata-v2-documentation/uri-conventions/#45_Filter_System_Query_Option_filter
#
#   FUNCTIONS
#       String: substringof, endswith, startswith, length, indexof, replace, substring, tolower, toupper, trim, concat
#       Date: day, hour, minute, month, second, year
#       Math: round, floor, ceiling
#
#   COMPARERS
#       ne, eq, lt, lte, gt, gte
#
#   OPERATORS
#       mod, add, sub, mul, div
#
#   LOGICAL
#       and, or, not
ODATA_TOKEN_SPLIT = re.compile("((?:[0-9]+\.[0-9]*)|(?:[0-9]*\.[0-9]+)|\w+|\(|\)|(?:'[^\']*'))")
# TODO: Consider implementing OData spec rather than Django ORM filters. Would we have to fork Django ORM?
ODATA_COMPARERS = {
    'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith',
    'exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull',
    'regex', 'iregex'
}
ODATA_LOGICAL = {'and', 'or'}


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
    def __init__(self, field, operator, literal):
        super(Predicate, self).__init__(field, lbp=0)
        self.field = field
        self.operator = operator
        self.literal = literal

    def nud(self, *args, **kwargs):
        lhs = '{0}{1}{2}'.format(self.field, LOOKUP_SEP, self.operator)
        return Q(**{lhs: self.literal})


class Infix(Symbol):
    def __init__(self, value, lbp=0, led=None):
        super(Infix, self).__init__(value, lbp)

        if callable(led):
            self.led = six.create_bound_method(led, self)


class Prefix(Symbol):
    def __init__(self, value, lbp=70, nud=None):
        super(Prefix, self).__init__(value, lbp)

        if callable(nud):
            self.nud = six.create_bound_method(nud, self)


def tokenize(string, inst):
    tokens = ODATA_TOKEN_SPLIT.findall(string)

    while len(tokens) > 0:
        token = tokens.pop(0)

        if token in Symbol._cache:
            yield Symbol._cache[token]
        else:
            raw_field = token

            try:
                operator = tokens.pop(0)
                raw_literal = tokens.pop(0)
            except IndexError:
                raise InvalidFilterError('Incomplete predicate format at: `{0}`'.format(raw_field))

            if not operator in ODATA_COMPARERS:
                raise InvalidFilterError('Unexpected filter function: `{0}`'.format(operator))

            field = inst.check_filtering(raw_field)
            literal = util.get_literal_value(raw_literal)

            yield Predicate(field, operator, literal)

    yield Symbol.get('(end)')


def or_led(self, lhs, expr, **kwargs):
    return lhs | expr(self.lbp)


def and_led(self, lhs, expr, **kwargs):
    return lhs & expr(self.lbp)


def not_nud(self, expr, **kwargs):
    return ~expr(self.lbp)


def lparen_nud(self, expr, match, **kwargs):
    value = expr()
    match(Symbol.get(')'))

    return value


if __name__:
    Symbol.register('(end)')
    Infix.register('or', 50, led=or_led)
    Infix.register('and', 60, led=and_led)
    Prefix.register('not', nud=not_nud)
    Prefix.register('(', 0, nud=lparen_nud)
    Prefix.register(')', 0)