import json
import os

from django.core.management.base import BaseCommand

from ografy.core import api as CoreAPI
from ografy.core.documents import EndpointDefinition, Provider
from ografy.settings import MONGO_FIXTURE_DIRS


MONGO_DIR = MONGO_FIXTURE_DIRS[0]
DEMO_FILE_NAME = 'main_fixtures.json'


def create_fixture_endpoint(temp_endpoint, provider_id):
    return EndpointDefinition(
        enabled_by_default=temp_endpoint['enabled_by_default'],
        mapping=temp_endpoint['mapping'],
        name=temp_endpoint['name'],
        parameter_description=temp_endpoint['parameter_description'],
        provider=provider_id,
        path=temp_endpoint['path'],
    )


def create_fixture_provider(provider):
    return Provider(
        auth_backend=provider['auth_backend'],
        auth_type=provider['auth_type'],
        backend_name=provider['backend_name'],
        client_callable=provider['client_callable'],
        description=provider['description'],
        domain=provider['domain'],
        name=provider['name'],
        scheme=provider['scheme'],
        tags=provider['tags']
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for provider in fixture_data['providers']:
        insert_provider = create_fixture_provider(provider)
        provider = CoreAPI.ProviderApi.post(insert_provider)
        provider_definitions = fixture_data['endpointDefinitions'][0]

        if provider['backend_name'] in provider_definitions:
            for endpoint in provider_definitions[provider['backend_name']]:
                insert_endpoint_definition = create_fixture_endpoint(endpoint, provider)
                endpoint = CoreAPI.EndpointDefinitionApi.post(insert_endpoint_definition)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
