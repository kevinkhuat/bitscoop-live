import datetime
import json
import os

from django.core.management.base import BaseCommand
from mongoengine import Q

from ografy.core import api as core_api
from ografy.core.documents import Event, Location, Signal
from ografy.settings import MONGO_FIXTURE_DIRS


MONGO_DIR = MONGO_FIXTURE_DIRS[0]
DEMO_FILE_NAME = 'demo_data.json'


def create_fixture_signal():
    return Signal(
        complete=True,
        connected=True,
        created=datetime.datetime.now,
        enabled=True,
        frequency=4,
        updated=datetime.datetime.now,
        user_id=0
    )


def create_fixture_event(temp_event, provider, signal):
    return Event(
        created=temp_event['created'],
        datetime=temp_event['datetime'],
        data_dict=temp_event['data_dict'],
        event_type=temp_event['event_type'],
        location=temp_event['location'],
        name=temp_event['name'],
        provider=provider,
        provider_name=temp_event['provider_name'],
        signal=signal,
        updated=temp_event['updated'],
        user_id=temp_event['user_id'],
    )


def create_fixture_location(event):
    return Location(
        datetime=event.datetime,
        geo_format=event['location']['geo_format'],
        geolocation=event['location']['geolocation'],
        reverse_geolocation=event['location']['reverse_geolocation'],
        reverse_geo_format=event['location']['reverse_geo_format'],
        resolution=event['location']['resolution'],
        source=str(event['id']),
        user_id=event.user_id
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    # A fake signal, created so that the test events' signal reference is to an actual object in the DB
    insert_signal = create_fixture_signal()
    temp_signal = core_api.SignalApi.post(insert_signal)

    for event in fixture_data['events']:
        temp_event = event['event']
        provider = core_api.ProviderApi.get(Q(name=temp_event['provider_name'])).get()
        signal = temp_signal
        insert_event = create_fixture_event(temp_event, provider, signal)

        insert_event = core_api.EventApi.post(insert_event)

        insert_location = create_fixture_location(insert_event)
        core_api.LocationApi.post(insert_location)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
