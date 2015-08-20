from bson.objectid import ObjectId
import datetime
import json
import os

from django.core.management.base import BaseCommand

from ografy.core import api as core_api
from ografy.core.documents import Contact, Content, Event, Location, Signal
from ografy.settings import FIXTURE_DIRS


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

    if hasattr(signal, 'access_token'):
        return_signal['access_token'] = signal['access_token']

    if hasattr(signal, 'oauth_token'):
        return_signal['oauth_token'] = signal['oauth_token']

    if hasattr(signal, 'oauth_token_secret'):
        return_signal['oauth_token_secret'] = signal['oauth_token_secret']

    if hasattr(signal, 'last_run'):
        return_signal['last_run'] = signal['last_run']

    return return_signal


def create_fixture_event(event):
    return_event = Event(
        id=ObjectId(event['_id']),
        contacts_list=event['contacts_list'],
        content_list=event['content_list'],
        created=event['created'],
        data_dict=event['data_dict'],
        datetime=event['datetime'],
        event_type=event['event_type'],
        location=event['location'],
        ografy_unique_id=event['ografy_unique_id'],
        provider=event['provider'],
        provider_name=event['provider_name'],
        signal=event['signal'],
        updated=event['updated'],
        user_id=event['user_id'],
    )

    return return_event


def create_fixture_location(location):
    return_location = Location(
        id=ObjectId(location['_id']),
        data_dict=location['data_dict'],
        datetime=location['datetime'],
        geo_format=location['geo_format'],
        geolocation=location['geolocation'],
        user_id=location['user_id'],
    )

    if hasattr(location, 'resolution'):
        return_location['resolution'] = location['resolution']

    return return_location


def create_fixture_contact(contact):
    return_contact = Contact(
        id=ObjectId(contact['_id']),
        data_dict=contact['data_dict'],
        ografy_unique_id=contact['ografy_unique_id'],
        signal=ObjectId(contact['signal']),
        updated=contact['updated'],
        user_id=contact['user_id']
    )

    if hasattr(contact, 'api_id'):
        Contact['api_id'] = contact['api_id']

    if hasattr(contact, 'handle'):
        Contact['handle'] = contact['handle']

    if hasattr(contact, 'name'):
        Contact['name'] = contact['name']

    return return_contact


def create_fixture_content(content):
    return_content = Content(
        id=ObjectId(content['_id']),
        content_type=content['content_type'],
        created=content['created'],
        data_dict=content['data_dict'],
        ografy_unique_id=content['ografy_unique_id'],
        signal=ObjectId(content['signal']),
        updated=content['updated'],
        user_id=content['user_id']
    )

    if hasattr(content, 'title'):
        return_content['title'] = content['title']

    if hasattr(content, 'url'):
        return_content['url'] = content['url']

    return return_content


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for signal in fixture_data['signals']:
        insert_signal = create_fixture_signal(signal)
        core_api.SignalApi.post(insert_signal)

    for contact in fixture_data['contacts']:
        insert_contact = create_fixture_contact(contact)
        core_api.ContactApi.post(insert_contact)

    for content in fixture_data['content']:
        insert_content = create_fixture_content(content)
        core_api.ContentApi.post(insert_content)

    for location in fixture_data['locations']:
        insert_location = create_fixture_location(location)
        core_api.LocationApi.post(insert_location)

    for event in fixture_data['events']:
        insert_event = create_fixture_event(event)
        core_api.EventApi.post(insert_event)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
