SEARCH_TEXT_FIELDS = (
    'contacts_list.handle',
    'contacts_list.name',
    'content_list.content_type',
    'content_list.file_extension',
    'content_list.owner',
    'content_list.text',
    'content_list.title',
    'content_list.url',
    'event_type',
    'provider_name',
)


SEARCH_VALIDATION_OBJECT = {
    'query': {
        'filtered': {
            'filter': {
                'and': [
                    {
                        'bool': {
                            'should': [
                                {
                                    'and': [
                                        {
                                            'or': [
                                                {
                                                    'term': {
                                                        'contacts_list.name': None
                                                    }
                                                },
                                                {
                                                    'term': {
                                                        'contacts_list.handle': None
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            'term': {
                                                'contact_interaction_type': None
                                            }
                                        }
                                    ]
                                },
                                {
                                    'term': {
                                        'content_list.content_type': None
                                    }
                                },
                                {
                                    'geo_distance': {
                                        'distance': None,
                                        'location.geolocation': {
                                            'lat': None,
                                            'lon': None
                                        }
                                    }
                                },
                                {
                                    'not': {
                                        'geo_distance': {
                                            'distance': None,
                                            'location.geolocation': {
                                                'lat': None,
                                                'lon': None
                                            }
                                        }
                                    }
                                },
                                {
                                    'not': {
                                        'geo_polygon': {
                                            'location.geolocation': {
                                                'points': [
                                                    {
                                                        'lat': None,
                                                        'lon': None
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                },
                                {
                                    'geo_polygon': {
                                        'location.geolocation': {
                                            'points': [
                                                {
                                                    'lat': None,
                                                    'lon': None
                                                }
                                            ]
                                        }
                                    }
                                },
                                {
                                    'range': {
                                        'datetime': {
                                            'format': None,
                                            'gte': None,
                                            'lte': None
                                        }
                                    }
                                },
                                {
                                    'term': {
                                        'provider_name': None
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
            'query': {
                'multi_match': {
                    'query': None,
                    'type': 'most_fields',
                    'fields': SEARCH_TEXT_FIELDS
                }
            }
        }
    },
    'size': None,
    'from': None
}
