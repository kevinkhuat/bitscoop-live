import os
import json

from django.core.management.base import BaseCommand

from ografy.apps.core import api as CoreAPI
from ografy.apps.core.documents import EndpointDefinition, Provider, Signal
from ografy.settings import MONGO_FIXTURE_DIRS


MONGO_DIR = MONGO_FIXTURE_DIRS[0]
DEMO_FILE_NAME = 'main_fixtures.json'


def create_fixture_endpoint(temp_endpoint, provider_id):
    return EndpointDefinition(
        name=temp_endpoint['name'],
        route_end=temp_endpoint['route_end'],
        provider=provider_id,
        parameter_description=temp_endpoint['parameter_description'],
        mapping=temp_endpoint['mapping'],
        enabled_by_default=temp_endpoint['enabled_by_default']
    )


def create_fixture_provider(provider):
    return Provider(
        name=provider['name'],
        base_route=provider['base_route'],
        backend_name=provider['backend_name'],
        auth_backend=provider['auth_backend'],
        auth_type=provider['auth_type'],
        client_callable=provider['client_callable'],
        description=provider['description'],
        tags=provider['tags']
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for provider in fixture_data['providers']:
        insert_provider = create_fixture_provider(provider)
        provider_id = CoreAPI.ProviderApi.post(insert_provider)['id']
        provider_definitions = fixture_data['endpointDefinitions'][0]

        if provider['backend_name'] in provider_definitions:
            for endpoint in provider_definitions[provider['backend_name']]:
                insert_endpoint_definition = create_fixture_endpoint(endpoint, provider_id)
                endpoint_id = CoreAPI.EndpointDefinitionApi.post(insert_endpoint_definition)['id']


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
