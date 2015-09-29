import json
import os
import urllib

import bson
from django.core.management.base import BaseCommand

from ografy.core import api as core_api
from ografy.core.documents import Endpoint, EventSource, Provider
from ografy.settings import FIXTURE_DIRS


FIXTURE_DIR = os.path.join(FIXTURE_DIRS[0], 'mongo', 'providers')


def create_fixture_endpoint(name, value, provider):
    scheme_and_domain = provider['domain'].split('://')
    url_parts = [''] * 6
    url_parts[0] = scheme_and_domain[0]
    url_parts[1] = scheme_and_domain[1]
    url_parts[2] = value['path']

    route = urllib.parse.urlunparse(url_parts)

    return_endpoint = Endpoint(
        call_method=value['call_method'],
        name=name,
        route=route,
    )

    if 'additional_path_fields' in value.keys():
        return_endpoint['additional_path_fields'] = value['additional_path_fields']

    if 'header_descriptions' in value.keys():
        return_endpoint['header_descriptions'] = value['header_descriptions']

    if 'parameter_descriptions' in value.keys():
        return_endpoint['parameter_descriptions'] = value['parameter_descriptions']

    if 'return_header_descriptions' in value.keys():
        return_endpoint['return_header_descriptions'] = value['return_header_descriptions']

    return return_endpoint


def create_fixture_event_source(name, value, endpoint_list):
    value_dict = {}
    event_source_endpoint_list = value['endpoints']

    for endpoint_name in event_source_endpoint_list:
        for endpoint in endpoint_list:
            if endpoint_name == endpoint['name']:
                value_dict[endpoint['name']] = endpoint

    return EventSource(
        description=value['description'],
        display_name=value['display_name'],
        enabled_by_default=value['enabled_by_default'],
        endpoints=value_dict,
        initial_mapping=value['initial_mapping'],
        mappings=value['mappings'],
        name=name
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
        tags=provider['tags']
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)
    endpoint_list = []
    event_source_list = []

    for name, value in fixture_data['endpoints'].items():
        insert_endpoint = create_fixture_endpoint(name, value, fixture_data['provider'])
        endpoint_list.append(insert_endpoint)

    for name, value in fixture_data['event_sources'].items():
        insert_event_source = create_fixture_event_source(name, value, endpoint_list)
        event_source_list.append(insert_event_source)

    insert_provider = create_fixture_provider(fixture_data['provider'], event_source_list)
    provider = core_api.ProviderApi.post(insert_provider)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_list = os.listdir(os.path.abspath(FIXTURE_DIR))

        for file in file_list:
            file_path = os.path.abspath(os.path.join(FIXTURE_DIR, file))
            load_fixture(file_path)
