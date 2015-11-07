from server.contrib.estoolbox.security.validators import FILTER_VALIDATOR


class InvalidDSLQueryException(Exception):
    pass


class InvalidTagExcpetion(Exception):
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


def validate_tags(document, field_validator):
    for key in field_validator.keys():
        if key in document.keys():
            field_value = document[key]
            validator_value = field_validator[key]

            # If the field contains only a single tag, and it's not in a list
            if not isinstance(field_value, list):
                # If this field is supposed to contain a list of tags, then there's an error
                if validator_value['many']:
                    raise InvalidTagExcpetion('Only one tag allowed, but a list of tags was provided')
                else:
                    pass
            elif isinstance(field_value, list):
                allowed_fields = validator_value['allowed']

                for item in field_value:
                    if item not in allowed_fields and item is not None:
                        raise InvalidTagExcpetion('An invalid tag was found')


def validate_dsl(query):
    _check_allowed_properties(query, FILTER_VALIDATOR)
