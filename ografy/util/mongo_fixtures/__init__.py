import json

from django.db.models import Q

import ografy.apps.obase.api as ObaseAPI

from ografy.apps.core import api as core_api
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.core.models import User, Signal

import datetime


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
        type=event_type,
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


def create_fixture_message(temp_message, event_id):
    return Message(
        message_to=temp_message['message_to'],
        message_from=temp_message['message_from'],
        message_body=temp_message['message_body'],
        user_id=temp_message['user_id'],
        event=event_id
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

    for message in fixture_data['messages']:
        temp_data = message['data']
        insert_data = create_fixture_data(temp_data)

        data_id = ObaseAPI.DataApi.post(insert_data)['id']

        temp_event = message['event']
        insert_event = create_fixture_event(temp_event, data_id, 'Message')

        event_id = ObaseAPI.EventApi.post(insert_event)['id']

        temp_message = message['message']
        insert_message = create_fixture_message(temp_message, event_id)

        message_id = ObaseAPI.MessageApi.post(insert_message)['id']
