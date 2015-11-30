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
                'index': 'not_analyzed'
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'handle': {
                'type': 'string'
            },
            'identifier': {  # How do we uniquely identify this contact for that provider. Provider & identifier used together to identify uniqueness on the index
                'type': 'string',
                'index': 'not_analyzed'
            },
            'name': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'remote_id': {  # Optional - Such as what is twitter's ID for this handle
                'type': 'string',
                'index': 'not_analyzed'
            },
            'source': {  # Optional - Endpoint the data came from and can be used to update it
                'type': 'string',
                'index': 'not_analyzed'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'user_id': {  # Optional
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'embed_content': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'embed_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'embed_thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'mimetype': {  # Optional
                'type': 'string'
            },
            'owner': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
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
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {  # Optional
                'type': 'long'
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
                'index': 'not_analyzed'
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
                        'index': 'not_analyzed'
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'handle': {
                        'type': 'string'
                    },
                    'name': {  # Optional
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    }
                }
            },
            'content': {  # Optional
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'embed_content': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'embed_format': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'embed_thumbnail': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
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
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'datetime': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'location': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'datetime': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'estimated': {
                        'type': 'boolean'
                    },
                    'geo_format': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'geolocation': {
                        'type': 'geo_point'
                    },
                    'resolution': {  # Optional
                        'type': 'float'
                    }
                }
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'places': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'location': {  # Optional
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'string',
                                'index': 'not_analyzed'
                            },
                            'geo_format': {
                                'type': 'string',
                                'index': 'not_analyzed'
                            },
                            'geolocation': {
                                'type': 'geo_point'
                            },
                            'resolution': {  # Optional
                                'type': 'float'
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
                        'index': 'not_analyzed'
                    },
                    'source': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'text': {  # Optional
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'updated': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'provider_name': {
                'type': 'string'
            },
            'things': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'created': {  # Optional
                        'type': 'date',
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'embed_content': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'embed_format': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'embed_thumbnail': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'locations': {  # Optional
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'string',
                                'index': 'not_analyzed'
                            },
                            'geo_format': {
                                'type': 'string',
                                'index': 'not_analyzed'
                            },
                            'geolocation': {
                                'type': 'geo_point'
                            },
                            'resolution': {  # Optional
                                'type': 'float'
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
                        'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
                    },
                    'url': {  # Optional
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            },
            'type': {
                'type': 'string'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'user_id': {
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'datetime': {
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'geo_format': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'geolocation': {
                'type': 'geo_point'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'resolution': {  # Optional
                'type': 'float'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {  # Optional - Only user specific when it's tied to events or collected user locations over time. Not user specific only if it is tied to a thing or place
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'contacts': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
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
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'name': {  # Optional
                'type': 'string'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'text': {  # Optional
                'type': 'string'
            },
            'thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {  # Optional
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'contacts': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
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
                'index': 'not_analyzed'
            },
            'provider': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'text': {  # Optional
                'type': 'string'
            },
            'thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {  # Optional
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'location': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'geo_format': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'geolocation': {
                        'type': 'geo_point'
                    },
                    'resolution': {  # Optional
                        'type': 'float'
                    }
                }
            },
            'name': {  # Optional
                'type': 'string'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'reverse_geolocation': {  # Optional
                'type': 'string'
            },
            'reverse_geo_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'text': {  # Optional
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'updated': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {  # Optional
                'type': 'long'
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
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'search_DSL': {
                'type': 'object',
                'dynamic': 'false'
            },
            'tags': {  # Optional
                'type': 'string'
            },
            'user_id': {
                'type': 'long'
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
                'index': 'not_analyzed'
            },
            'created': {  # Optional
                'type': 'date',
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'embed_content': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'embed_format': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'embed_thumbnail': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'locations': {  # Optional
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'geo_format': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'geolocation': {
                        'type': 'geo_point'
                    },
                    'resolution': {  # Optional
                        'type': 'float'
                    }
                }
            },
            'identifier': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'owner': {  # Optional
                'type': 'string'
            },
            'remote_id': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'source': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
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
                'format': 'yyyy-MM-dd\'T\'HH:mm:ss.SSSZ'
            },
            'url': {  # Optional
                'type': 'string',
                'index': 'not_analyzed'
            },
            'user_id': {
                'type': 'long'
            }
        }
    }
}
