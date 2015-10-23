CONTENT_TAG_VALIDATOR = {
    'type': {
        'allowed': {
            'audio',
            'code',
            'file',
            'game',
            'other',
            'photo',
            'receipt',
            'software',
            'text',
            'video',
            'web-page',
        },
        'many': False
    }
}


EVENT_TAG_VALIDATOR = {
    'contact_interaction_type': {
        'allowed': {
            'from',
            'to',
            'with',
        },
        'many': False
    },
    'type': {
        'allowed': {
            'call',
            'comment',
            'create',
            'edit',
            'message',
            'play',
            'view',
        },
        'many': False
    }
}


GROUP_TAG_VALIDATOR = {
    'type': {
        'allowed': {
            'colleagues',
            'family',
            'friends',
        },
        'many': False
    }
}


ORGANIZATION_TAG_VALIDATOR = {
    'type': {
        'allowed': {
            'products',
            'products-services',
            'services',
        },
        'many': False
    }
}


PLACE_TAG_VALIDATOR = {
    'reverse_geo_format': {
        'allowed': {
            'address',
            'city',
            'county',
            'country',
            'international-area',
            'proper-name',
            'proper-name-address',
            'unincorporated',
        },
        'many': False
    },
    'type': {
        'allowed': {
            'business',
            'public',
            'residential',
        },
        'many': False,
    }
}


THING_TAG_VALIDATOR = {
    'type': {
        'allowed': {
            'apparel-accessories',
            'appliances',
            'automotive',
            'baby',
            'books-magazines',
            'electronics',
            'food',
            'gifts',
            'health-beauty',
            'home-kitchen',
            'movies-tv',
            'music',
            'office',
            'pet',
            'sports-outdoors',
            'tickets-events',
            'tools-home-improvement',
            'toys-games',
        },
        'many': True
    }
}


SEARCH_TEXT_FIELDS = [
    'contacts.handle',
    'contacts.name',
    'content.type',
    'content.file_extension',
    'content.owner',
    'content.text',
    'content.title',
    'content.url',
    'things.title',
    'things.text',
    'type',
    'provider_name',
]


FILTER_VALIDATOR = {
    'bool': {
        'should': [
            {
                'and': [
                    {
                        'or': [
                            {
                                'term': {
                                    'contacts.name': None
                                }
                            },
                            {
                                'term': {
                                    'contacts.handle': None
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
                            'contacts.name': None
                        }
                    },
                    {
                        'term': {
                            'contacts.handle': None
                        }
                    }
                ]
            },
            {
                'term': {
                    'content.type': None
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
