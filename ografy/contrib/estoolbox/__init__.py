EVENT_MAPPING = {
    '_id': {
        'path': 'id'
    },
    'properties': {
        'created': {
            'type': 'date',
            'format': 'YYYY-MM-DD\'T\'HH:mm:ss.SSSZ'
        },
        'datetime': {
            'type': 'date',
            'format': 'YYYY-MM-DD\'T\'HH:mm:ss.SSSZ'
        },
        'event_type': {
            'type': 'string'
        },
        'id': {
            'type': 'string'
        },
        'location': {
            'type': 'geo_point'
        },
        'name': {
            'type': 'string'
        },
        'provider': {
            'type': 'string'
        },
        'provider_name': {
            'type': 'string'
        },
        'signal': {
            'type': 'string'
        },
        'subtype': {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'object',
                    'properties': {
                        'message_body': {
                            'type': 'string'
                        },
                        'message_from': {
                            'type': 'string'
                        },
                        'message_to': {
                            'type': 'string'
                        },
                        'message_type': {
                            'type': 'string'
                        },
                    }
                },
                'play': {
                    'type': 'object',
                    'properties': {
                        'media_url': {
                            'type': 'string'
                        },
                        'play_type': {
                            'type': 'string'
                        },
                        'title': {
                            'type': 'string'
                        },
                    }
                }
            }
        },
        'updated': {
            'type': 'string',
            'format': 'YYYY-MM-DD\'T\'HH:mm:ss.SSSZ'
        },
        'user_id': {
            'type': 'long'
        }
    }
}

# https://www.elastic.co/guide/en/elasticsearch/guide/current/combining-filters.html

FILTERS = [
    'should',
    'must',
    'must_not'
]

# https://www.elastic.co/guide/en/elasticsearch/guide/current/querying-geo-shapes.html

GEO_FILTERS = {
    'circle': {
        'within',
        'without'
    },
    'polygon': {
        'within',
        'without'
    },
}

MAPPED_FIELDS = {
    'event': [
        'id',
        'authorized_endpoint',
        'created',
        'datetime',
        'event_type',
        'location',
        'name',
        'provider',
        'provider_name',
        'signal',
        'updated',
        'user_id'
    ],
    'message': [
        'message_body',
        'message_from',
        'message_to',
        'message_type'
    ],
    'play': [
        'media_url',
        'play_type',
        'title'
    ]
}

MAPPED_SEARCH_FIELDS = {
    'event': {
        'id',
        'authorized_endpoint',
        'created',
        'datetime',
        'event_type',
        'name',
        'provider',
        'provider_name',
        'signal',
        'updated'
    },
    'message': {
        'message_body',
        'message_from',
        'message_to',
        'message_type'
    },
    'play': {
        'media_url',
        'play_type',
        'title'
    }
}

MAPPED_SEARCH_TEXT_FIELDS = [
    'event.name',
    'event.provider_name',
    'message.message_body',
    'message.message_from',
    'message.message_to',
    'play.media_url',
    'play.title'
]

MAPPED_SEARCH_GEO_FIELDS = {
    'event': {
        'location'
    }
}

RANGE_FILTERS = [
    'gt',
    'lt',
    'gte',
    'lte'
]

TEMPLATE_QUERY_STRUCTURED = {
    'query': {
        'filtered': {
            'filter': {
                'bool': {}
            }
        }
    }
}

TEMPLATE_QUERY_FULL_TEXT = {
    'multi_match': {
        'query': '',
        'type': 'most_fields',
        'fields': MAPPED_SEARCH_TEXT_FIELDS
    }
}
