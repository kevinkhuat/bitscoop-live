import datetime
import json
import os

from django.core.management.base import BaseCommand
from mongoengine import Q

from ografy.core import api as CoreAPI
from ografy.core.documents import Data, Event, Message, Play, Signal
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


def create_fixture_data(temp_data, event):
    return Data(
        created=temp_data['created'],
        data_blob=temp_data['data_blob'],
        event=event,
        updated=temp_data['updated'],
        user_id=temp_data['user_id'],
    )


def create_fixture_event(temp_event, provider, signal):
    return Event(
        created=temp_event['created'],
        datetime=temp_event['datetime'],
        event_type=temp_event['event_type'],
        location=temp_event['location'],
        name=temp_event['name'],
        provider=provider,
        provider_name=temp_event['provider_name'],
        signal=signal,
        updated=temp_event['updated'],
        user_id=temp_event['user_id'],
    )


def create_fixture_message(temp_message, event):
    return Message(
        event=event,
        message_body=temp_message['message_body'],
        message_from=temp_message['message_from'],
        message_to=temp_message['message_to'],
        message_type=temp_message['message_type'],
        user_id=temp_message['user_id'],
    )


def create_fixture_play(temp_play, event):
    return Play(
        event=event,
        play_type=temp_play['play_type'],
        title=temp_play['title'],
        user_id=temp_play['user_id'],
        # media_url=temp_play['media_url']
    )


def load_fixture(path):
    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    # A fake signal, created so that the test events' signal reference is to an actual object in the DB
    insert_signal = create_fixture_signal()
    temp_signal = CoreAPI.SignalApi.post(insert_signal)

    for event in fixture_data['events']:
        temp_event = event['event']
        provider = CoreAPI.ProviderApi.get(Q(name=temp_event['provider_name'])).get()
        signal = temp_signal
        insert_event = create_fixture_event(temp_event, provider, signal)

        insert_event = CoreAPI.EventApi.post(insert_event)

        temp_data = event['data']
        insert_data = create_fixture_data(temp_data, insert_event)

        data = CoreAPI.DataApi.post(insert_data)  # noqa

    for message in fixture_data['messages']:
        temp_event = message['event']
        provider = CoreAPI.ProviderApi.get(Q(name=temp_event['provider_name'])).get()
        signal = temp_signal
        insert_event = create_fixture_event(temp_event, provider, signal)

        insert_event = CoreAPI.EventApi.post(insert_event)

        temp_data = message['data']
        insert_data = create_fixture_data(temp_data, insert_event)

        data = CoreAPI.DataApi.post(insert_data)  # noqa

        temp_message = message['message']
        insert_message = create_fixture_message(temp_message, insert_event)

        message = CoreAPI.MessageApi.post(insert_message)  # noqa

    for play in fixture_data['plays']:
        temp_event = play['event']
        provider = CoreAPI.ProviderApi.get(Q(name=temp_event['provider_name'])).get()
        signal = temp_signal
        insert_event = create_fixture_event(temp_event, provider, signal)

        insert_event = CoreAPI.EventApi.post(insert_event)

        temp_data = play['data']
        insert_data = create_fixture_data(temp_data, insert_event)

        data = CoreAPI.DataApi.post(insert_data)  # noqa

        temp_play = play['play']
        insert_play = create_fixture_play(temp_play, insert_event)

        play = CoreAPI.PlayApi.post(insert_play)  # noqa


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.abspath(os.path.join(MONGO_DIR, DEMO_FILE_NAME))
        load_fixture(file_path)
