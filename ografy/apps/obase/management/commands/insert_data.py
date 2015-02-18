import json
import ografy.apps.obase.api as ObaseAPI
from ografy.apps.obase.documents import Data, Event
from django.core.management.base import BaseCommand, CommandError
from bson.objectid import ObjectId

import datetime

mongo_dir = '../../../fixtures_mongo'


class Command(BaseCommand):
    def handle(self, *args, **options):
        demo_data_file = open(mongo_dir + '/demoData.json', encoding='utf-8').read()

        demo_data = json.loads(demo_data_file)

        for event in demo_data['events']:
            if hasattr(event, 'event'):
                demo_event =Event(
                    user_id=1,
                    created=datetime.datetime(2014, 12, 1, 19, 54, 6),
                    updated=datetime.datetime(2014, 12, 1, 19, 54, 6),
                    signal_id=2,
                    provider_id=3,
                    provider_name='steam',
                    datetime=datetime.datetime(2014, 12, 1, 19, 54, 6),
                    data=ObjectId("54d110db4b757538b165763a"),
                    name='Thomas',
                    location=[-73.68, 40.68832]
                )
                ObaseAPI.EventApi.post(demo_event)

# test_data=Event(
#     user_id=1,
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
#     user_id=1,
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
#     user_id=1,
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
#     user_id=1,
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
#     user_id=1,
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
#     user_id=1,
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
