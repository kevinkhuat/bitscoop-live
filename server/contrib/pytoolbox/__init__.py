import re


PATTERN = re.compile('[.$]')


def strip_invalid_key_characters(input_dict):
    for key in input_dict:
        if isinstance(key, str):
            match = re.search(PATTERN, key)
            if match:
                new_key = re.sub(PATTERN, '*dot*', key)
                input_dict[new_key] = input_dict.pop(key)
                key = new_key

        if isinstance(input_dict[key], list):
            for item in input_dict[key]:
                if isinstance(item, dict):
                    item = strip_invalid_key_characters(item)
        elif isinstance(input_dict[key], dict):
            input_dict[key] = strip_invalid_key_characters(input_dict[key])

    return input_dict


def initialize_endpoint_data(provider, connection, source, endpoint, population):
    connection['endpoint_data'][source][endpoint] = {}

    for parameter, values in provider['endpoints'][endpoint]['parameters'].items():
        if 'default' in values.keys():
            connection['endpoint_data'][source][endpoint][parameter] = values['default']

    for field, values in provider['endpoints'][endpoint]['model']['fields'].items():
        if isinstance(values, dict) and values['type'] == 'related' and (population == '*' or values['ref'] == population):
            initialize_endpoint_data(provider, connection, source, values['ref'], '*')
