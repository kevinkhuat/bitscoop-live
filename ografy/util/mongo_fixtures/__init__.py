import json

from bson.objectid import ObjectId
from django.db.models import Q

import ografy.apps.obase.api as ObaseAPI

from ografy.apps.core import api as core_api
from ografy.apps.core.models import Signal
from ografy.apps.obase.documents import Data, Event, Message
from ografy.apps.core.models import User, Signal, Provider

import datetime


def load_fixture(path):

	demo_data_file = open(path, encoding='utf-8').read()

	demo_data = json.loads(demo_data_file)

	#Create a demo user
	demo_user = User(
		id=2,
		email='demouser@demo.com',
		handle='DemoUser',
		first_name='Demo',
		last_name='User',
		date_joined=datetime.datetime(2015, 2, 25, 16, 14, 15),
		is_staff=False,
		is_active=True,
		is_verified=True,
		password_date=datetime.datetime(2015, 2, 25, 16, 14, 15)
	)

	demo_user.set_password('DemoUser')
	demo_user.save()
	#Create a list of demo signals

	for signal_dict in demo_data['signals']:
		user = core_api.UserApi.get(Q(id=signal_dict['user'])).get()
		provider = core_api.ProviderApi.get(Q(id=signal_dict['provider'])).get()
		signal = Signal(
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
		signal.save()

	test_data = Data(
		created=datetime.datetime(2014, 12, 31, 15, 22, 24),
		updated=datetime.datetime(2014, 12, 31, 15, 22, 24),
		user_id=2,
		data_blob={"d": {"array": [1, 2, 3], "boolean": True, "null": None, "number": 123, "object": {"a": "b", "c": "d", "e": "f"}, "string": "Hello World"}}
	)

	test_event = Event(
		user_id=2,
		created=datetime.datetime(2014, 12, 31, 15, 22, 24),
		updated=datetime.datetime(2014, 12, 31, 15, 22, 24),
		signal_id=4,
		provider_id=5,
		provider_name='dropbox',
		datetime=datetime.datetime(2014, 12, 31, 15, 22, 24),
		name='Uploaded file "Big Air"',
		location=[-73.68855, 40.68719]
	)

	test_message = Message(
		user_id=2,
		message_to=["Sarah"],
		message_from="John",
		message_body="I am done with Justin Bieber"
	)

	test_data_json = test_data.to_json()

	test_data_from_json = Data.from_json(test_data_json)

	test_event_json = test_event.to_json()

	test_event_from_json = Event.from_json(test_event_json)

	test_message_json = test_message.to_json()

	test_message_from_json = Message.from_json(test_message_json)

	for event in demo_data['events']:
		temp_data = event['data']
		insert_data = Data(
			created=temp_data['created'],
			updated=temp_data['updated'],
			user_id=temp_data['user_id'],
			data_blob=temp_data['data_blob']
		)

		data_id = ObaseAPI.DataApi.post(insert_data)['id']

		temp_event = event['event']
		insert_event = Event(
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

		event_id = ObaseAPI.EventApi.post(insert_event)['id']

	for message in demo_data['messages']:
		temp_data = message['data']
		insert_data = Data(
			created=temp_data['created'],
			updated=temp_data['updated'],
			user_id=temp_data['user_id'],
			data_blob=temp_data['data_blob']
		)

		data_id = ObaseAPI.DataApi.post(insert_data)['id']

		temp_event = message['event']
		insert_event = Event(
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

		event_id = ObaseAPI.EventApi.post(insert_event)['id']

		temp_message = message['message']
		insert_message = Message(
			message_to=temp_message['message_to'],
			message_from=temp_message['message_from'],
			message_body=temp_message['message_body'],
			user_id=temp_message['user_id'],
			event=event_id
		)

		message_id = ObaseAPI.MessageApi.post(insert_message)['id']

# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2013, 2, 1, 11, 23, 6),
#     updated=datetime.datetime(2013, 4, 1, 13, 2, 6),
#     signal_id=2,
#     provider_id=3,
#     provider_name='steam',
#     datetime=datetime.datetime(2013, 4, 1, 13, 2, 6),
#     data=ObjectId("54d110db4b757538b165763b"),
#     name='Sam',
#     location=[-73.687, 40.68830]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 12, 1, 19, 54, 6),
#     updated=datetime.datetime(2014, 12, 1, 19, 54, 6),
#     signal_id=1,
#     provider_id=1,
#     provider_name='facebook',
#     datetime=datetime.datetime(2014, 12, 1, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b165763c"),
#     name='Sam',
#     location=[-73.68, 40.68717]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 12, 3, 19, 54, 6),
#     updated=datetime.datetime(2014, 12, 3, 19, 54, 6),
#     signal_id=1,
#     provider_id=1,
#     provider_name='facebook',
#     datetime=datetime.datetime(2014, 12, 3, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b165763d"),
#     name='John',
#     location=[-73.68, 40.68888]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 12, 8, 19, 54, 6),
#     updated=datetime.datetime(2014, 12, 8, 19, 54, 6),
#     signal_id=3,
#     provider_id=8,
#     provider_name='github',
#     datetime=datetime.datetime(2014, 12, 8, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b165763e"),
#     name='Sam',
#     location=[-73.683, 40.68844]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 11, 3, 19, 54, 6),
#     updated=datetime.datetime(2014, 11, 3, 19, 54, 6),
#     signal_id=1,
#     provider_id=1,
#     provider_name='facebook',
#     datetime=datetime.datetime(2014, 11, 3, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b165763f"),
#     name='John',
#     location=[-73.68, 40.68852]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 3, 2, 19, 54, 6),
#     updated=datetime.datetime(2014, 3, 2, 19, 54, 6),
#     signal_id=4,
#     provider_id=2,
#     provider_name='twitter',
#     datetime=datetime.datetime(2014, 3, 2, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b1657640"),
#     name='Samantha',
#     location=[-73.682, 40.68890]
# )
#
# ObaseAPI.EventApi.post(test_data)
#
# test_data=Event(
#     user_id=2,
#     created=datetime.datetime(2014, 12, 14, 19, 54, 6),
#     updated=datetime.datetime(2014, 12, 14, 19, 54, 6),
#     signal_id=2,
#     provider_id=3,
#     provider_name='steam',
#     datetime=datetime.datetime(2014, 12, 14, 19, 54, 6),
#     data=ObjectId("54d110db4b757538b1657641"),
#     name='John',
#     location=[-93.67, 40.68831]
# )
#
# ObaseAPI.EventApi.post(test_data)

# from ografy.lib.smokesignal.parsers import Parser
#
# from pprint import pprint
#
#
# steam_test_mapping = open('data/steam/steam_test_mapping.json', encoding='utf-8').read()
# twitter_test_mapping = open('data/twitter/twitter_test_mapping.json', encoding='utf-8').read()
# facebook_test_mapping = open('data/facebook/facebook_test_mapping.json', encoding='utf-8').read()
#
# steam_GetFriendList = open('data/steam/GetFriendList.json', encoding='utf-8').read()
# steam_GetPlayerSummaries = open('data/steam/GetPlayerSummaries.json', encoding='utf-8').read()
# steam_GetRecentlyPlayedGames = open('data/steam/GetRecentlyPlayedGames.json', encoding='utf-8').read()
#
# twitter_friends_List = open('data/twitter/friends/list.json', encoding='utf-8').read()
# twitter_status_user_timeline = open('data/twitter/status/user_timeline.json', encoding='utf-8').read()
#
# facebook_me = open('data/facebook/me.json', encoding='utf-8').read()
# facebook_me_friends = open('data/facebook/me/friends.json', encoding='utf-8').read()
# facebook_me_inbox = open('data/facebook/me/inbox.json', encoding='utf-8').read()
# facebook_me_outbox = open('data/facebook/me/outbox.json', encoding='utf-8').read()
#
# steam_parser = Parser.create("Steam", "Steam", steam_test_mapping)
# twitter_parser = Parser.create("Twitter", "Twitter", twitter_test_mapping)
# facebook_parser = Parser.create("facebook", "facebook", facebook_test_mapping)
#
# pprint("Dynamic Steam Parser Testing")
# pprint(steam_parser.GetPlayerSummaries(steam_GetPlayerSummaries))
# pprint(steam_parser.GetFriendList(steam_GetFriendList))
# pprint(steam_parser.GetRecentlyPlayedGames(steam_GetRecentlyPlayedGames))
#
# pprint("Dynamic Twitter Parser Testing")
# pprint(twitter_parser.friends_list(twitter_friends_List))
# pprint(twitter_parser.status_user_timeline(twitter_status_user_timeline))
#
# pprint("Dynamic Facebook Parser Testing")
# pprint(facebook_parser.me(facebook_me))
# pprint(facebook_parser.me_friends(facebook_me_friends))
# pprint(facebook_parser.me_inbox(facebook_me_inbox))
