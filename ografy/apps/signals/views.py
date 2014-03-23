from __future__ import unicode_literals
import copy
import json
from pprint import pprint

from ografy.apps.core import models
from django.conf import settings
from django.http import HttpResponse

# from smokesignal.parsers import Parser
#
#
# def parse_steam(account):
#     # steam_test_mapping = open('../smokesignal/tests/data/steam/steam_test_mapping.json', encoding='utf-8').read()
#     # steam_GetFriendList = open('../smokesignal/tests/data/steam/GetFriendList.json', encoding='utf-8').read()
#     # steam_GetPlayerSummaries = open('../smokesignal/tests/data/steam/GetPlayerSummaries.json', encoding='utf-8').read()
#     # steam_GetRecentlyPlayedGames = open('../smokesignal/tests/data/steam/GetRecentlyPlayedGames.json', encoding='utf-8').read()
#     # steam_parser = Parser.create('Steam', 'Steam', steam_test_mapping)
#     # pprint('Dynamic Steam Parser Testing')
#     # player_summaries_list = steam_parser.GetPlayerSummaries(steam_GetPlayerSummaries)
#     # pprint(player_summaries_list)
#
#     metric_summs = []
#     # for summ in player_summaries_list:
#         # metric_summ = models.Metric(account=account, url=url, update_date=update_date)
#         # metric_summs.append(metric_summ)
#
#
#     # pprint(steam_parser.GetFriendList(steam_GetFriendList))
#     # pprint(steam_parser.GetRecentlyPlayedGames(steam_GetRecentlyPlayedGames))
#
#
# def parse_twitter():
#     twitter_test_mapping = open('../smokesignal/tests/data/twitter/twitter_test_mapping.json', encoding='utf-8').read()
#     twitter_friends_List = open('../smokesignal/tests/data/twitter/friends/list.json', encoding='utf-8').read()
#     twitter_status_user_timeline = open('../smokesignal/tests/data/twitter/status/user_timeline.json', encoding='utf-8').read()
#     twitter_parser = Parser.create('Twitter', 'Twitter', twitter_test_mapping)
#     pprint('Dynamic Twitter Parser Testing')
#     pprint(twitter_parser.friends_list(twitter_friends_List))
#     pprint(twitter_parser.status_user_timeline(twitter_status_user_timeline))
#
#
# def parse_facebook():
#     facebook_test_mapping = open('../smokesignal/tests/data/facebook/facebook_test_mapping.json', encoding='utf-8').read()
#     facebook_me = open('../smokesignal/tests/data/facebook/me.json', encoding='utf-8').read()
#     facebook_me_friends = open('../smokesignal/tests/data/facebook/me/friends.json', encoding='utf-8').read()
#     facebook_me_inbox = open('../smokesignal/tests/data/facebook/me/inbox.json', encoding='utf-8').read()
#     facebook_me_outbox = open('../smokesignal/tests/data/facebook/me/outbox.json', encoding='utf-8').read()
#     facebook_parser = Parser.create('facebook', 'facebook', facebook_test_mapping)
#     pprint('Dynamic Facebook Parser Testing')
#     pprint(facebook_parser.me(facebook_me))
#     pprint(facebook_parser.me_friends(facebook_me_friends))
#     pprint(facebook_parser.me_inbox(facebook_me_inbox))


def index(request):
    # config = copy.deepcopy(settings.SIGNALS)
    # return HttpResponse(json.dumps(config), content_type='application/json')
    user = models.User(email='test@email.com', email='upper@email.com', first_name='test',
                       last_name='tests')
    account = models.Account(user=user, name='steam', root_url='')

    # parse_steam(account)

    return HttpResponse('Now Parsing')
