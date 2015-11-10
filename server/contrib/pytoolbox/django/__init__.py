def get_content_type(accepted_types, types={'text/html'}, default_type='text/html'):
    response_type = default_type

    for type in accepted_types:
        if type in types:
            response_type = type
            break

    return response_type
