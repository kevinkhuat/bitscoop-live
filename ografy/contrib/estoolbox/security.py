from ografy.contrib.estoolbox import SEARCH_VALIDATION_OBJECT


class InvalidDSLQueryException(Exception):
    pass


def _check_allowed_properties(query, validation_query):
    if isinstance(query, dict):
        for attr, value in query.items():
            if attr not in validation_query.keys():
                raise InvalidDSLQueryException('Invalid DSL query. Please check the documentation')
            elif validation_query[attr] is not None:
                _check_allowed_properties(value, validation_query[attr])
    elif isinstance(query, list) or isinstance(query, set):
        success = False

        for query_item in query:
            if isinstance(query_item, str) or isinstance(query_item, float) or isinstance(query_item, int):
                if query_item not in validation_query:
                    raise InvalidDSLQueryException('Invalid DSL query. Please check the documentation')
            else:
                for validation_item in validation_query:
                    try:
                        _check_allowed_properties(query_item, validation_item)
                        success = True
                        break
                    except InvalidDSLQueryException:
                        pass

                if not success:
                    raise InvalidDSLQueryException('Invalid DSL query. Please check the documentation')
    elif isinstance(query, str):
        if query != validation_query:
            raise InvalidDSLQueryException('Invalid DSL query. Please check the documentation')
    else:
        raise InvalidDSLQueryException('Invalid DSL query. Please check the documentation')


def validate_dsl(query):
    _check_allowed_properties(query, SEARCH_VALIDATION_OBJECT)
