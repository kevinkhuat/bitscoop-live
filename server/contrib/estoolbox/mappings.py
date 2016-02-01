# TODO:
# Add Group
# Add Transaction
# Edit Event to add Group, Organization, Transaction and replace Contact with People
# Edit Organization to be of groups and not contacts

CONTACT_MAPPING = {
    'contact': {
        'dynamic': 'false',
        'properties': {
            'connection': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'handle': {
                'type': 'string'
            },
            'identifier': {  # How do we uniquely identify this contact for that provider. Provider & identifier used together to identify uniqueness on the index
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'name': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'remote_id': {  # Optional - Such as what is twitter's ID for this handle
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'source': {  # Optional - Endpoint the data came from and can be used to update it
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'user_id': {  # Optional
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
            'connection': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'embed_content': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'embed_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'embed_thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'mimetype': {  # Optional
                'type': 'string'
            },
            'owner': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {  # Optional
                'type': 'string'
            },
            'title': {  # Optional
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {  # Optional
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
            'connection': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'contact_interaction_type': {  # Optional
                'type': 'string'
            },
            'context': {  # Optional
                'type': 'string'
            },
            'contacts': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'handle': {
                        'type': 'string'
                    },
                    'name': {  # Optional
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    }
                }
            },
            'content': {  # Optional
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'embed_content': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'embed_format': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'embed_thumbnail': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'mimetype': {  # Optional
                        'type': 'string'
                    },
                    'owner': {  # Optional
                        'type': 'string'
                    },
                    'text': {  # Optional
                        'type': 'string'
                    },
                    'title': {  # Optional
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    }
                }
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'datetime': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'location': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'datetime': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'estimated': {
                        'type': 'boolean',
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
                    'resolution': {  # Optional
                        'type': 'float',
                        'doc_values': True
                    }
                }
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'places': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'location': {  # Optional
                        'type': 'object',
                        'properties': {
                            'id': {
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
                            'resolution': {  # Optional
                                'type': 'float',
                                'doc_values': True
                            }
                        }
                    },
                    'name': {  # Optional
                        'type': 'string'
                    },
                    'reverse_geolocation': {  # Optional
                        'type': 'string'
                    },
                    'reverse_geo_format': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'source': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'text': {  # Optional
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
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
            'things': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'embed_content': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'embed_format': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'embed_thumbnail': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'locations': {  # Optional
                        'type': 'object',
                        'properties': {
                            'id': {
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
                            'resolution': {  # Optional
                                'type': 'float',
                                'doc_values': True
                            }
                        }
                    },
                    'owner': {  # Optional
                        'type': 'string'
                    },
                    'text': {  # Optional
                        'type': 'string'
                    },
                    'title': {  # Optional
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                        'doc_values': True
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    }
                }
            },
            'type': {
                'type': 'string'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'updated': {  # Optional
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
            'connection': {  # Optional - Location might be generated by us, in which case no connection
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
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
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'resolution': {  # Optional
                'type': 'float',
                'doc_values': True
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {  # Optional - Only user specific when it's tied to events or collected user locations over time. Not user specific only if it is tied to a thing or place
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
            'connection': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'contacts': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'handle': {
                        'type': 'string'
                    },
                    'name': {  # Optional
                        'type': 'string'
                    }
                }
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'name': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {  # Optional
                'type': 'string'
            },
            'thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {  # Optional
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
            'age': {  # Optional
                'type': 'integer'
            },
            'connection': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'contacts': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'doc_values': True
                    },
                    'handle': {
                        'type': 'string'
                    },
                    'name': {  # Optional
                        'type': 'string'
                    }
                }
            },
            'first_name': {  # Optional
                'type': 'string'
            },
            'gender': {  # Optional
                'type': 'string'
            },
            'last_name': {  # Optional
                'type': 'string'
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {  # Optional
                'type': 'string'
            },
            'thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {  # Optional
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
            'connection': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'location': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
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
                    'resolution': {  # Optional
                        'type': 'float',
                        'doc_values': True
                    }
                }
            },
            'name': {  # Optional
                'type': 'string'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'reverse_geolocation': {  # Optional
                'type': 'string'
            },
            'reverse_geo_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {  # Optional
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'user_id': {  # Optional
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
            'tags': {  # Optional
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
            'connection': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'embed_content': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'embed_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'embed_thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'locations': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
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
                    'resolution': {  # Optional
                        'type': 'float',
                        'doc_values': True
                    }
                }
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'owner': {  # Optional
                'type': 'string'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed',
                'doc_values': True
            },
            'text': {  # Optional
                'type': 'string'
            },
            'title': {  # Optional
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ',
                'doc_values': True
            },
            'url': {  # Optional
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
