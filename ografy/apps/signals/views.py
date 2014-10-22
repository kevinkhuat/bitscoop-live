from __future__ import unicode_literals
import copy
import json
import six
import datetime
import random
import string
import urllib

from pprint import pprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from ografy.apps.core.models import Account, Metric, Entry, Message
from ografy.lib.smokesignal.parsers import Parser

BANK = string.ascii_uppercase + string.ascii_lowercase + string.digits


#TODO: Conform to https://docs.djangoproject.com/en/dev/topics/serialization/
def rand_string(length=15):
    return ''.join(random.choice(BANK) for x in range(length))


def parse_steam(account):
    steam_test_mapping = open('../smokesignal/tests/data/steam/steam_test_mapping.json', encoding='utf-8').read()
    # steam_GetFriendList = open('../smokesignal/tests/data/steam/GetFriendList.json', encoding='utf-8').read()
    # steam_GetPlayerSummaries = open('../smokesignal/tests/data/steam/GetPlayerSummaries.json', encoding='utf-8').read()
    # steam_GetRecentlyPlayedGames = open('../smokesignal/tests/data/steam/GetRecentlyPlayedGames.json',encoding='utf-8').read()
    steam_parser = Parser.create('Steam', 'Steam', steam_test_mapping)

    return_list = []

    # #TODO: change to event?
    # player_summaries_list = steam_parser.GetPlayerSummaries(steam_GetPlayerSummaries)
    # metric_summs = []
    # for summary in player_summaries_list.get('playerSummaries'):
    #     metric_summ = Metric(account=account, url='steam.com', update_date=datetime.datetime.now(),
    #                          stat_name='friend', stat_value=summary.get('lastlogoff'))
    #     metric_summs.append(metric_summ)
    #     return_list.append(model_to_dict(metric_summ))
    #     metric_summ.save()
    #
    # friends_list = steam_parser.GetFriendList(steam_GetFriendList)
    # entry_friends = []
    # for friend in friends_list.get('friendList'):
    #     entry_friend = Entry(account=account, url='steam.com', datetime=datetime.datetime.now(),
    #                          entry_name='lastlogoff', data=friend.get('name'),
    #                          vid=rand_string(), update_date=datetime.datetime.now())
    #     entry_friends.append(entry_friend)
    #     return_list.append(model_to_dict(entry_friend))
    #     entry_friend.save()
    #
    # played_game_list = steam_parser.GetRecentlyPlayedGames(steam_GetRecentlyPlayedGames)
    # entry_games = []
    # for game in played_game_list.get('games'):
    #     entry_game = Entry(account=account, url='steam.com', datetime=datetime.datetime.now(),
    #                        entry_name='name', data=game.get('name'),
    #                        vid=rand_string(), update_date=datetime.datetime.now())
    #     entry_games.append(entry_game)
    #     return_list.append(model_to_dict(entry_game))
    #     entry_game.save()
    #
    # pprint('Dynamic Steam Parser Testing')
    # pprint(metric_summs)
    # pprint(entry_friends)
    # pprint(entry_friends)

    return return_list


def parse_twitter(twitter_data):
    twitter_test_mapping = open('../smokesignal/tests/data/twitter/twitter_test_mapping.json', encoding='utf-8').read()
    # twitter_friends_List = open('../smokesignal/tests/data/twitter/friends/list.json', encoding='utf-8').read()
    # twitter_status_user_timeline = open('../smokesignal/tests/data/twitter/status/user_timeline.json',
    #                                     encoding='utf-8').read()
    twitter_parser = Parser.create('Twitter', 'Twitter', twitter_test_mapping)
    friends_list = twitter_parser.friends_list(twitter_data['friends'])


def parse_facebook(facebook_data):
    facebook_test_mapping = open('../smokesignal/tests/data/facebook/facebook_test_mapping.json',
                                 encoding='utf-8').read()
    # facebook_me = open('../smokesignal/tests/data/facebook/me.json', encoding='utf-8').read()
    # facebook_me_friends = open('../smokesignal/tests/data/facebook/me/friends.json', encoding='utf-8').read()
    # facebook_me_inbox = open('../smokesignal/tests/data/facebook/me/inbox.json', encoding='utf-8').read()
    # facebook_me_outbox = open('../smokesignal/tests/data/facebook/me/outbox.json', encoding='utf-8').read()

    facebook_parser = Parser.create('facebook', 'facebook', facebook_test_mapping)

    facebook_parser.me(facebook_data['me'])
    facebook_parser.me_friends(facebook_data['user-friends'])
    facebook_parser.me_likes(facebook_data['user-likes'])
    facebook_parser.me_inbox(facebook_data['inbox'])
    facebook_parser.me_outbox(facebook_data['outbox'])


def index(request):
    # return render(request, 'oauthtest.html')
    config = open('../ografy/tests/smokesignal/data/test-configs/test-config-1.json', encoding='utf-8').read()
    return HttpResponse(config, content_type='application/json')


@csrf_exempt
def server_get(request):
    if request.method == 'POST':
        try:
            # assuming request.body contains json data which is UTF-8 encoded
            url = request.body.decode()
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            resp_obj = response.read()
            resp_str = resp_obj.decode("utf-8")
            return HttpResponse(resp_str, content_type='application/json')
        except Exception:
            return HttpResponse("ERROR", content_type='application/json')
    return HttpResponse("NOT POST", content_type='text')


@csrf_exempt
def signal_facebook(request):
    if request.method == 'POST':
         # assuming request.body contains json data which is UTF-8 encoded
        json_data = json.loads(request.body.decode())
        # parse_facebook(json_data)
        return HttpResponse("Facebook Success", content_type='application/json')
    return HttpResponse("NOT POST", content_type='text')


@csrf_exempt
def signal_twitter(request):
    if request.method == 'POST':
         # assuming request.body contains json data which is UTF-8 encoded
        json_data = json.loads(request.body.decode())
        # parse_twitter(json_data)
        return HttpResponse("Twitter Success", content_type='application/json')
    return HttpResponse("NOT POST", content_type='text')


@csrf_exempt
def signal_steam(request):
    if request.method == 'POST':
         # assuming request.body contains json data which is UTF-8 encoded
        json_data = json.loads(request.body.decode())
        # parse_steam(json_data)
        return HttpResponse("Steam Success", content_type='application/json')
    return HttpResponse("NOT POST", content_type='text')
