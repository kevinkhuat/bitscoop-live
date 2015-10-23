CONTACT_MAPPING = {
    'contact': {
        'dynamic': 'false',
        'properties': {
            'api_id': {
                'type': 'string'
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'handle': {
                'type': 'string'
            },
            'name': {
                'type': 'string'
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
        'dynamic': 'false',
        'properties': {
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data': {
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
            'type': {
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
        'dynamic': 'false',
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
        'dynamic': 'false',
        'properties': {
            'contact_interaction_type': {
                'type': 'string'
            },
            'contacts': {
                'properties': {
                    'api_id': {
                        'type': 'string'
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
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    }
                }
            },
            'content': {
                'properties': {
                    'content': {
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
                        'type': 'string'
                    },
                    'owner': {
                        'type': 'string'
                    },
                    'text': {
                        'type': 'string'
                    },
                    'title': {
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {
                        'type': 'string'
                    }
                }
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'datetime': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
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
            'places': {
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
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'provider_name': {
                'type': 'string'
            },
            'things': {
                'properties': {
                    'created': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'owner': {
                        'type': 'string'
                    },
                    'text': {
                        'type': 'string'
                    },
                    'thing': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'title': {
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {
                        'type': 'string'
                    }
                }
            },
            'type': {
                'type': 'string'
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
        'dynamic': 'false',
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


ORGANIZATION_MAPPING = {
    'organization': {
        'dynamic': 'false',
        'properties': {
            'contacts': {
                'properties': {
                    'api_id': {
                        'type': 'string'
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
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    }
                }
            },
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'name': {
                'type': 'string'
            },
            'ografy_user_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {
                'type': 'string'
            },
            'type': {
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


PERSON_MAPPING = {
    'person': {
        'dynamic': 'false',
        'properties': {
            'age': {
                'type': 'integer'
            },
            'contacts': {
                'properties': {
                    'api_id': {
                        'type': 'string'
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
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'updated': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    }
                }
            },
            'first_name': {
                'type': 'string'
            },
            'gender': {
                'type': 'string'
            },
            'last_name': {
                'type': 'string'
            },
            'ografy_user_id': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {
                'type': 'string'
            },
            'user_id': {
                'type': 'long',
                'doc_values': True
            }
        }
    }
}

PLACE_MAPPING = {
    'place': {
        'dynamic': 'false',
        'properties': {
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data': {
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
            'name': {
                'type': 'string'
            },
            'reverse_geolocation': {
                'type': 'string'
            },
            'reverse_geo_format': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'signal': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {
                'type': 'string'
            },
            'type': {
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
        'dynamic': 'false',
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

THING_MAPPING = {
    'thing': {
        'dynamic': 'false',
        'properties': {
            'created': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'data': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'locations': {
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
            'type': {
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
