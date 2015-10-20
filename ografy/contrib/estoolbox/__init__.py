SEARCH_TEXT_FIELDS = [
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
]


SEARCH_VALIDATION_OBJECT = {
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
                    'contact_interaction_type': None
                }
            },
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
                        'time_zone': None,
                        'format': None,
                        'gte': None,
                        'lte': None
                    }
                }
            },
            {
                'term': {
                    'signal': None
                }
            }
        ],
        'must': [],
        'must_not': []
    }
}


CONTACT_MAPPING = {
    'contact': {
        'properties': {
            'api_id': {
                'type': 'string'
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data_id_list': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'handle': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'name': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'ografy_unique_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'updated': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}


CONTENT_MAPPING = {
    'content': {
        'properties': {
            'content_type': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data_id_list': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'file_extension': {
                'type': 'string'
            },
            'ografy_unique_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'owner': {
                'type': 'string'
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {
                'type': 'string'
            },
            'title': {
                'type': 'string'
            },
            'updated': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'url': {
                'type': 'string'
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}


DATA_MAPPING = {
    'data': {
        'properties': {
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data_dict': {
                'type': 'object',
                'dynamic': 'false'
            },
            'ografy_unique_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'updated': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}


EVENT_MAPPING = {
    'event': {
        'properties': {
            'contact_interaction_type': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'contacts_list': {
                'properties': {
                    'api_id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'contact': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'handle': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'name': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    }
                }
            },
            'content_list': {
                'properties': {
                    'content': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'content_type': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'file_extension': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'owner': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'text': {
                        'type': 'string'
                    },
                    'title': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    }
                }
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data_id_list': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'datetime': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'event_type': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'location': {
                'type': 'object',
                'properties': {
                    'estimated': {
                        'type': 'boolean',
                        'doc_values': True
                    },
                    'estimation_method': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'geo_format': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'geolocation': {
                        'type': 'geo_point',
                        'doc_values': True
                    },
                    'location': {
                        'type': 'string'
                    },
                    'resolution': {
                        'type': 'float',
                        'doc_values': True
                    }
                }
            },
            'ografy_unique_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'provider_name': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'updated': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}


LOCATION_MAPPING = {
    'location': {
        'properties': {
            'datetime': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'geo_format': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'geolocation': {
                'type': 'geo_point',
                'doc_values': True
            },
            'resolution': {
                'type': 'float',
                'doc_values': True
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'source': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}

SEARCH_MAPPING = {
    'search': {
        'properties': {
            'datetime': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'search_DSL': {
                'type': 'object',
                'dynamic': 'false'
            },
            'tags': {
                'type': 'string'
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}
