import json
import os

from django.core.management.base import BaseCommand

from ografy.apps.core import api as CoreAPI
from ografy.apps.core.documents import Data, Event, Message, Play
from ografy.settings import MONGO_FIXTURE_DIRS


MONGO_DIR = MONGO_FIXTURE_DIRS[0]
DEMO_FILE_NAME = 'demo_data.json'


def create_fixture_data(temp_data):
    return Data(
        created=temp_data['created'],
        updated=temp_data['updated'],
        user_id=temp_data['user_id'],
        data_blob=temp_data['data_blob']
    )


def create_fixture_event(temp_event, data):
    return Event(
        event_type=temp_event['event_type'],
        created=temp_event['created'],
        updated=temp_event['updated'],
        user_id=temp_event['user_id'],
        datetime=temp_event['datetime'],
        location=temp_event['location'],
        name=temp_event['name'],
        provider_id=temp_event['provider_id'],
        provider_name=temp_event['provider_name'],
        signal_id=temp_event['signal_id'],
        data=data
    )


def create_fixture_message(temp_message, event):
    return Message(
        user_id=temp_message['user_id'],
        event=event,
        message_type=temp_message['message_type'],
        message_to=temp_message['message_to'],
        message_from=temp_message['message_from'],
        message_body=temp_message['message_body']
    )


def create_fixture_play(temp_play, event):
    return Play(
        event=event,
        user_id=temp_play['user_id'],
        play_type=temp_play['play_type'],
        title=temp_play['title']
        # media_url=temp_play['media_url']
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    for event in fixture_data['events']:
        temp_data = event['data']
        insert_data = create_fixture_data(temp_data)

        data = CoreAPI.DataApi.post(insert_data)

        temp_event = event['event']
        insert_event = create_fixture_event(temp_event, data)

        event_id = CoreAPI.EventApi.post(insert_event)['id']
        CoreAPI.DataApi.patch(data['id'], {'event_id': event_id})

    for message in fixture_data['messages']:
        temp_data = message['data']
        insert_data = create_fixture_data(temp_data)

        data_id = CoreAPI.DataApi.post(insert_data)['id']

        temp_event = message['event']
        insert_event = create_fixture_event(temp_event, data_id)

        event_id = CoreAPI.EventApi.post(insert_event)['id']
        CoreAPI.DataApi.patch(data_id, {'event_id': event_id})

        temp_message = message['message']
        insert_message = create_fixture_message(temp_message, event_id)

        message_id = CoreAPI.MessageApi.post(insert_message)['id']
        CoreAPI.EventApi.patch(event_id, {'subtype_id': message_id})

    for play in fixture_data['plays']:
        temp_data = play['data']
        insert_data = create_fixture_data(temp_data)

        data_id = CoreAPI.DataApi.post(insert_data)['id']

        temp_event = play['event']
        insert_event = create_fixture_event(temp_event, data_id)

        event_id = CoreAPI.EventApi.post(insert_event)['id']
        CoreAPI.DataApi.patch(data_id, {'event_id': event_id})

        temp_play = play['play']
        insert_play = create_fixture_play(temp_play, event_id)

        play_id = CoreAPI.PlayApi.post(insert_play)['id']
        CoreAPI.EventApi.patch(event_id, {'subtype_id': play_id})


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
