import datetime
import json
import os
import urllib

import bson
from django.core.management.base import BaseCommand

from ografy.core import api as core_api
from ografy.core.documents import Endpoint, EventSource, Provider, Settings
from ografy.settings import FIXTURE_DIRS


FIXTURE_DIR = os.path.join(FIXTURE_DIRS[0], 'mongo', 'providers')


def create_fixture_endpoint(temp_endpoint, provider):
    url_parts = [''] * 6
    url_parts[0] = provider['scheme']
    url_parts[1] = provider['domain']
    url_parts[2] = temp_endpoint['path']

    route = urllib.parse.urlunparse(url_parts)

    if 'additional_path_fields' in temp_endpoint.keys():
        return Endpoint(
            additional_path_fields=temp_endpoint['additional_path_fields'],
            call_method=temp_endpoint['call_method'],
            name=temp_endpoint['name'],
            parameter_descriptions=temp_endpoint['parameter_descriptions'],
            route=route,
        )
    else:
        return Endpoint(
            call_method=temp_endpoint['call_method'],
            name=temp_endpoint['name'],
            parameter_descriptions=temp_endpoint['parameter_descriptions'],
            route=route,
        )


def create_fixture_event_source(temp_event_source, endpoint_list):
    temp_endpoint_dict = {}
    event_source_endpoint_list = temp_event_source['endpoints']

    for endpoint_name in event_source_endpoint_list:
        for endpoint in endpoint_list:
            if endpoint_name == endpoint['name']:
                temp_endpoint_dict[endpoint['name']] = endpoint

    return EventSource(
        description=temp_event_source['description'],
        display_name=temp_event_source['display_name'],
        enabled_by_default=temp_event_source['enabled_by_default'],
        endpoints=temp_endpoint_dict,
        initial_mapping=temp_event_source['initial_mapping'],
        mappings=temp_event_source['mappings'],
        name=temp_event_source['name']
    )


def create_fixture_provider(provider, event_source_list):
    event_source_dict = {}

    for event_source in event_source_list:
        event_source_dict[event_source['name']] = event_source

    return Provider(
        auth_backend=provider['auth_backend'],
        auth_type=provider['auth_type'],
        backend_name=provider['backend_name'],
        client_callable=provider['client_callable'],
        description=provider['description'],
        endpoint_wait_time=provider['endpoint_wait_time'],
        event_sources=event_source_dict,
        domain=provider['domain'],
        name=provider['name'],
        provider_number=bson.ObjectId(provider['provider_number']),
        scheme=provider['scheme'],
        tags=provider['tags'],
        url_name=provider['url_name']
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


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)
    endpoint_list = []
    event_source_list = []

    for endpoint in fixture_data['endpoints']:
        insert_endpoint = create_fixture_endpoint(endpoint, fixture_data['provider'])
        endpoint_list.append(insert_endpoint)

    for event_source in fixture_data['event_sources']:
        insert_event_source = create_fixture_event_source(event_source, endpoint_list)
        event_source_list.append(insert_event_source)

    insert_provider = create_fixture_provider(fixture_data['provider'], event_source_list)
    provider = core_api.ProviderApi.post(insert_provider)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_list = os.listdir(os.path.abspath(FIXTURE_DIR))

        for file in file_list:
            file_path = os.path.abspath(os.path.join(FIXTURE_DIR, file))
            load_fixture(file_path)

        insert_settings = create_fixture_settings()
        core_api.SettingsApi.post(insert_settings)
