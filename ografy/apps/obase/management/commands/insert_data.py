import os
import json
import datetime

import ografy.apps.obase.api as ObaseAPI

from django.db.models import Q
from django.core.management.base import BaseCommand

from ografy.apps.core import api as core_api
from ografy.apps.obase.documents import Data, Event, Message, Play
from ografy.apps.core.models import User, Signal


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MONGO_DIR = os.path.join(CURRENT_DIR, '../../fixtures_mongo')

DEMO_FILE_NAME = 'demoData.json'




def create_demo_user():
    return User(
        id=2,
        email='demouser@demo.com',
        handle='DemoUser',
        first_name='Demo',
        last_name='User',
        date_joined=datetime.datetime(2015, 2, 25, 16, 14, 15),
        is_staff=False,
        is_active=True,
        is_verified=True,
        password_date=datetime.datetime(2015, 2, 25, 16, 14, 15),
        last_login=datetime.datetime(2015, 2, 25, 16, 14, 15)
    )


def create_fixture_signal(signal_dict, user, provider):
    return Signal(
        user=user,
        provider=provider,
        name=signal_dict['name'],
        psa_backend_uid=signal_dict['psa_backend_uid'],
        complete=signal_dict['complete'],
        connected=signal_dict['connected'],
        enabled=signal_dict['enabled'],
        frequency=signal_dict['frequency'],
        created=signal_dict['created'],
        updated=signal_dict['updated']
    )


def create_fixture_data(temp_data):
    return Data(
        created=temp_data['created'],
        updated=temp_data['updated'],
        user_id=temp_data['user_id'],
        data_blob=temp_data['data_blob']
    )

def create_fixture_event(temp_event, data_id, event_type='Event'):
    return Event(
        created=temp_event['created'],
        updated=temp_event['updated'],
        user_id=temp_event['user_id'],
        datetime=temp_event['datetime'],
        location=temp_event['location'],
        name=temp_event['name'],
        provider_id=temp_event['provider_id'],
        provider_name=temp_event['provider_name'],
        signal_id=temp_event['signal_id'],
        data=data_id
    )


def create_fixture_message(temp_message, data_id):
    return Message(
        created=temp_message['created'],
        updated=temp_message['updated'],
        user_id=temp_message['user_id'],
        datetime=temp_message['datetime'],
        location=temp_message['location'],
        name=temp_message['name'],
        provider_id=temp_message['provider_id'],
        provider_name=temp_message['provider_name'],
        signal_id=temp_message['signal_id'],
        data=data_id,
        message_to=temp_message['message_to'],
        message_from=temp_message['message_from'],
        message_body=temp_message['message_body']
    )


def create_fixture_play(temp_play, data_id):
    return Play(
        created=temp_play['created'],
        updated=temp_play['updated'],
        user_id=temp_play['user_id'],
        datetime=temp_play['datetime'],
        location=temp_play['location'],
        name=temp_play['name'],
        provider_id=temp_play['provider_id'],
        provider_name=temp_play['provider_name'],
        signal_id=temp_play['signal_id'],
        data=data_id,
        title=temp_play['title']
    )


def load_fixture(path):

    fixture_data_file = open(path, encoding='utf-8').read()
    fixture_data = json.loads(fixture_data_file)

    fixture_user = create_demo_user()

    fixture_user.set_password('DemoUser')
    fixture_user.save()

    for signal_dict in fixture_data['signals']:
        user = core_api.UserApi.get(Q(id=signal_dict['user'])).get()
        provider = core_api.ProviderApi.get(Q(id=signal_dict['provider'])).get()
        signal = create_fixture_signal(signal_dict, user, provider)
        signal.save()

    for event in fixture_data['events']:
        temp_data = event['data']
        insert_data = create_fixture_data(temp_data)

        data_id = ObaseAPI.DataApi.post(insert_data)['id']

        temp_event = event['event']
        insert_event = create_fixture_event(temp_event, data_id)

        event_id = ObaseAPI.EventApi.post(insert_event)['id']
        ObaseAPI.DataApi.patch(data_id, {'event_id': event_id})

    for message in fixture_data['messages']:
        temp_data = message['data']
        insert_data = create_fixture_data(temp_data)

        data_id = ObaseAPI.DataApi.post(insert_data)['id']

        temp_message = message['message']
        insert_message = create_fixture_message(temp_message, data_id)

        message_id = ObaseAPI.MessageApi.post(insert_message)['id']

    for play in fixture_data['plays']:
        temp_data = play['data']
        insert_data = create_fixture_data(temp_data)

        data_id = ObaseAPI.DataApi.post(insert_data)['id']

        temp_play = play['play']
        insert_play = create_fixture_play(temp_play, data_id)

        play_id = ObaseAPI.PlayApi.post(insert_play)['id']


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = os.path.abspath(MONGO_DIR + '/' + DEMO_FILE_NAME)
        load_fixture(file_path)