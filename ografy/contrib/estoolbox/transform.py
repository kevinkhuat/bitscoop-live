import copy
import re

from ografy.contrib.estoolbox import (
    FILTERS, GEO_FILTERS, MAPPED_SEARCH_FIELDS, MAPPED_SEARCH_GEO_FIELDS, RANGE_FILTERS, TEMPLATE_QUERY_FULL_TEXT,
    TEMPLATE_QUERY_STRUCTURED
)


# Internal function to add a search term to an explicit query "datTime 6/15/15"
def _add_term(key, val):
    return {
        'term': {
            key: val
        }
    }


# Internal function to add a range search term to an explicit query such as "datetime gte 6/15/15"
def _add_range(range_val, key, val):
    return {
        'range': {
            key: {
                range_val: val
            }
        }
    }


# Internal function to add an approved set of filters to the transformed query such as
# "must event.datetime gte 6/15/15 should event.provider facebook must_not provider twitter should event.location circle within 10km [11.113,-133.22] sort event.datetime asc"
def _structured_query_to_dsl(transformed_query, q_array):
    i = 0

    # For every delimited search element
    while i < len(q_array):

        # look for sort term
        element = q_array[i].lower()
        if element == 'sort':
            value = q_array[i + 1].lower()
            if value in MAPPED_SEARCH_FIELDS:
                transformed_query['sort'] = []
                transformed_query['sort'].append(
                    {
                        value: {
                            'order': q_array[i + 2].lower()
                        }
                    }
                )
                i += 3
        elif element == 'limit':
            value = q_array[i + 1]
            transformed_query['from'] = 0
            transformed_query['size'] = value
            i += 2
        else:
            query_filter = q_array[i + 1].lower()
            value = q_array[i + 2]

            # Look for actual filters for on approved terms
            if element in MAPPED_SEARCH_FIELDS and query_filter in FILTERS:
                # See if the filter is for a range of values
                # TODO: Support multiple ranges
                if value in RANGE_FILTERS:
                    range_val = value
                    value = q_array[i + 3]
                    i += 4
                    new_range = _add_range(range_val, element, value)
                    transformed_query['query']['filtered']['filter']['and'].append({'range': new_range['range']})
                # If not a range, add the filter term
                else:
                    i += 3
                    transformed_query['query']['filtered']['filter']['and']['bool'][query_filter] += _add_term(element, value)

            # Is it an approved geo filter?
            # TODO: Add ranges to geo filters and add more geo filters such as square
            elif element in MAPPED_SEARCH_GEO_FIELDS and query_filter in GEO_FILTERS:
                radius = 0
                relation = value
                value = q_array[i + 3]
                if query_filter is 'circle':
                    radius = q_array[i + 3]
                    value = q_array[i + 4]
                    i += 4
                i += 3
                if relation in GEO_FILTERS[query_filter]:
                    transformed_query.filter['geo_shape'] = {
                        'location': {
                            'relation': relation,
                            'shape': {
                                'type': query_filter,
                                'coordinates': value
                            }
                        }
                    }

                    if query_filter is 'circle':
                        transformed_query.filter['geo_shape']['location']['shape']['radius'] = radius
    return transformed_query


# Add user ID filter
def add_user_filter(query, user_id):
    return query['query']['filtered']['filter']['and'].append(
        {
            'bool': {
                'must': _add_term('user_id', user_id)
            }
        }
    )


# Creates a query of a full text search across all text approved fields
def transform_text_search(query, user_id=None):
    # use a base template to begin to structure query object
    transformed_query = copy.deepcopy(TEMPLATE_QUERY_STRUCTURED)
    transformed_query = add_user_filter(transformed_query, user_id)

    # Break up query by whitespace not surrounded by quotes
    q_array = re.split('[^\s]|"[\s]*"|\'[\s]*\'', query)

    transformed_query.update(TEMPLATE_QUERY_FULL_TEXT)
    transformed_query['multi_match']['query'] = q_array

    return transformed_query


def transform_structured_search(query, user_id=None):
    # use a base template to begin to structure query object
    transformed_query = copy.deepcopy(TEMPLATE_QUERY_STRUCTURED)

    # Break up query by whitespace not surrounded by quotes
    q_array = re.split('[^\s]|"[\s]*"|\'[\s]*\'', query)
    transformed_query = add_user_filter(transformed_query, user_id)

    return _structured_query_to_dsl(transformed_query, q_array)


def _check_allowed_properties(object, allowed_fields):
    for attr, value in object.__dict__.iteritems():
        if attr not in allowed_fields:
            raise Exception('Invalid DSL query. Please check the documentation')


def transform_validate_dsl(query, user_id=None):

    _check_allowed_properties(query, ['sort', 'limit', 'query', 'geo_shape'])

    if hasattr(query, 'query'):
        _check_allowed_properties(query.query, ['filtered'])
        if hasattr(query['query'], 'filter'):
            _check_allowed_properties(query.query.filtered, ['and'])
            if hasattr(query['query']['filter']['and'], 'bool'):
                _check_allowed_properties(query, MAPPED_SEARCH_FIELDS)

    if hasattr(query, 'geo_shape'):
        _check_allowed_properties(query.geo_shape, MAPPED_SEARCH_GEO_FIELDS)

    return add_user_filter(query, user_id)
