def clean_data(spec, data):
    insert_data = {}

    for key, value in spec:
        # Can the value be multiple types?
        if isinstance(value['type'], list):
            for type_val in value['type']:
                if isinstance(data[key], type_val):
                    insert_data[key] = data[key] | value['default']

        # Is it one type?
        elif isinstance(data[key], value['type']):
            insert_data[key] = data[key]

        # Just put the default
        else:
            insert_data[key] = value['default']

    return insert_data
