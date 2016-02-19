import json

from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

from server.contrib.estoolbox.mappings import (
    CONTACT_MAPPING, CONTENT_MAPPING, EVENT_MAPPING, LOCATION_MAPPING, ORGANIZATION_MAPPING, PERSON_MAPPING,
    PLACE_MAPPING, SEARCH_MAPPING, THING_MAPPING
)


es_connection = Elasticsearch([
    {
        'host': 'localhost',
        'port': 9200
    }
])


class Command(BaseCommand):
    def handle(self, *args, **options):
        es_connection.indices.put_mapping(
            index='core',
            doc_type='organization',
            body=json.dumps(ORGANIZATION_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='contact',
            body=json.dumps(CONTACT_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='content',
            body=json.dumps(CONTENT_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='event',
            body=json.dumps(EVENT_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='location',
            body=json.dumps(LOCATION_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='person',
            body=json.dumps(PERSON_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='place',
            body=json.dumps(PLACE_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='search',
            body=json.dumps(SEARCH_MAPPING)
        )

        es_connection.indices.put_mapping(
            index='core',
            doc_type='thing',
            body=json.dumps(THING_MAPPING)
        )
