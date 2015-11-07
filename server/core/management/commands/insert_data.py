import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

from server.core import api as core_api
from server.core.documents import Settings, Signal
from server.settings import FIXTURE_DIRS


es = Elasticsearch([{
    'host': settings.ELASTICSEARCH['HOST'],
    'port': settings.ELASTICSEARCH['PORT']
}])

MONGO_DIR = os.path.join(FIXTURE_DIRS[0], 'mongo')
DEMO_FILE_NAME = 'demo_data.json'


def create_fixture_signal(signal):
    return_signal = Signal(
        id=signal['_id'],
        complete=signal['complete'],
        connected=signal['connected'],
        created=signal['created'],
        enabled=signal['enabled'],
        endpoint_data=signal['endpoint_data'],
        frequency=signal['frequency'],
        name=signal['name'],
        permissions=signal['permissions'],
        provider=signal['provider'],
        signal_data=signal['signal_data'],
        updated=signal['updated'],
        user_id=signal['user_id'],
    )

    if 'access_token' in signal.keys():
        return_signal['access_token'] = signal['access_token']

    if 'oauth_token' in signal.keys():
        return_signal['oauth_token'] = signal['oauth_token']

    if 'oauth_token_secret' in signal.keys():
        return_signal['oauth_token_secret'] = signal['oauth_token_secret']

    if 'last_run' in signal.keys():
        return_signal['last_run'] = signal['last_run']

    return return_signal


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for signal in fixture_data['signals']:
        insert_signal = create_fixture_signal(signal)
        core_api.SignalApi.post(insert_signal)

    for data in fixture_data['data']:
        id = data['_id']
        del data['_id']

        es.index(
            index='core',
            id=id,
            doc_type='data',
            body=data
        )

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
