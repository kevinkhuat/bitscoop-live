import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

from server.core import api as core_api
from server.core.documents import Connection, Settings
from server.settings import FIXTURE_DIRS


es = Elasticsearch([{
    'host': settings.ELASTICSEARCH['HOST'],
    'port': settings.ELASTICSEARCH['PORT']
}])

MONGO_DIR = os.path.join(FIXTURE_DIRS[0], 'mongo')
DEMO_FILE_NAME = 'demo_data.json'


def create_fixture_connection(connection):
    return_connection = Connection(
        id=connection['_id'],
        auth_data=connection['auth_data'],
        auth_status={
            'complete': connection['auth_status']['complete'],
            'connected': connection['auth_status']['connected']
        },
        created=connection['created'],
        enabled=connection['enabled'],
        endpoint_data=connection['endpoint_data'],
        frequency=connection['frequency'],
        metadata=connection['metadata'],
        name=connection['name'],
        permissions=connection['permissions'],
        provider=connection['provider'],
        updated=connection['updated'],
        user_id=connection['user_id'],
    )

    if 'last_run' in connection.keys():
        return_connection['last_run'] = connection['last_run']

    return return_connection


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for connection in fixture_data['connections']:
        insert_connection = create_fixture_connection(connection)
        core_api.ConnectionApi.post(insert_connection)

    for contact in fixture_data['contacts']:
        id = contact['_id']
        del contact['_id']

        es.index(
            index='core',
            id=id,
            doc_type='contact',
            body=contact
        )

    for content in fixture_data['content']:
        id = content['_id']
        del content['_id']

        es.index(
            index='core',
            id=id,
            doc_type='content',
            body=content
        )

    for location in fixture_data['locations']:
        id = location['_id']
        del location['_id']

        es.index(
            index='core',
            id=id,
            doc_type='location',
            body=location
        )

    for organization in fixture_data['organizations']:
        id = organization['_id']
        del organization['_id']

        es.index(
            index='core',
            id=id,
            doc_type='organization',
            body=organization
        )

    for place in fixture_data['places']:
        id = place['_id']
        del place['_id']

        es.index(
            index='core',
            id=id,
            doc_type='place',
            body=place
        )

    for thing in fixture_data['things']:
        id = thing['_id']
        del thing['_id']

        es.index(
            index='core',
            id=id,
            doc_type='thing',
            body=thing
        )

    for event in fixture_data['events']:
        id = event['_id']
        del event['_id']

        es.index(
            index='core',
            id=id,
            doc_type='event',
            body=event
        )


def create_fixture_settings():
    return Settings(
        allow_location_collection=True,
        created=datetime.datetime.now,
        last_estimate_all_locations=datetime.datetime.now,
        location_estimation_method='Last',
        updated=datetime.datetime.now,
        user_id=1
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)

        insert_settings = create_fixture_settings()
        core_api.SettingsApi.post(insert_settings)
