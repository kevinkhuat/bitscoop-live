from __future__ import unicode_literals
import copy
import json
import six
import datetime
import random
import string

from pprint import pprint
from django.http import HttpResponse, StreamingHttpResponse
from django.forms.models import model_to_dict
from ografy.apps.core.models import Account, Metric, Entry, Message
from ografy.lib.xauth.models import User
from smokesignal.parsers import Parser


#TODO: Conform to https://docs.djangoproject.com/en/dev/topics/serialization/


BANK = string.ascii_uppercase + string.ascii_lowercase + string.digits
def rand_string(length=15):
    return ''.join(random.choice(BANK) for x in range(length))



def parse_steam(account):
    steam_test_mapping = open('../smokesignal/tests/data/steam/steam_test_mapping.json', encoding='utf-8').read()
    steam_GetFriendList = open('../smokesignal/tests/data/steam/GetFriendList.json', encoding='utf-8').read()
    steam_GetPlayerSummaries = open('../smokesignal/tests/data/steam/GetPlayerSummaries.json', encoding='utf-8').read()
    steam_GetRecentlyPlayedGames = open('../smokesignal/tests/data/steam/GetRecentlyPlayedGames.json', encoding='utf-8').read()
    steam_parser = Parser.create('Steam', 'Steam', steam_test_mapping)

    return_list = []

    #TODO: change to event?
    player_summaries_list = steam_parser.GetPlayerSummaries(steam_GetPlayerSummaries)
    metric_summs = []
    for summary in player_summaries_list.get('playerSummaries'):
        metric_summ = Metric(account=account, url='steam.com', update_date=datetime.datetime.now(),
                             stat_name='friend', stat_value=summary.get('lastlogoff'))
        metric_summs.append(metric_summ)
        return_list.append(model_to_dict(metric_summ))
        metric_summ.save()

    friends_list = steam_parser.GetFriendList(steam_GetFriendList)
    entry_friends = []
    for friend in friends_list.get('friendList'):
        entry_friend = Entry(account=account, url='steam.com', datetime=datetime.datetime.now(),
                             entry_name='lastlogoff', data=friend.get('name'),
                             vid=rand_string(), update_date=datetime.datetime.now())
        entry_friends.append(entry_friend)
        return_list.append(model_to_dict(entry_friend))
        entry_friend.save()

    played_game_list = steam_parser.GetRecentlyPlayedGames(steam_GetRecentlyPlayedGames)
    entry_games = []
    for game in played_game_list.get('games'):
        entry_game = Entry(account=account, url='steam.com', datetime=datetime.datetime.now(),
                           entry_name='name', data=game.get('name'),
                           vid=rand_string(), update_date=datetime.datetime.now())
        entry_games.append(entry_game)
        return_list.append(model_to_dict(entry_game))
        entry_game.save()

    pprint('Dynamic Steam Parser Testing')
    pprint(metric_summs)
    pprint(entry_friends)
    pprint(entry_friends)

    return return_list


def parse_twitter(account):
    twitter_test_mapping = open('../smokesignal/tests/data/twitter/twitter_test_mapping.json', encoding='utf-8').read()
    twitter_friends_List = open('../smokesignal/tests/data/twitter/friends/list.json', encoding='utf-8').read()
    twitter_status_user_timeline = open('../smokesignal/tests/data/twitter/status/user_timeline.json', encoding='utf-8').read()
    twitter_parser = Parser.create('Twitter', 'Twitter', twitter_test_mapping)

    return_list = []

    friends_list = twitter_parser.friends_list(twitter_friends_List)
    entry_friends = []
    for friend in friends_list.get('users'):
        entry_friend = Entry(account=account, url='twitter.com', datetime=datetime.datetime.now(),
                             entry_name='screen_name', data=friend.get('screen_name'),
                             vid=rand_string(), update_date=datetime.datetime.now())
        entry_friends.append(entry_friend)
        return_list.append(model_to_dict(entry_friend))
        entry_friend.save()

    tweet_list = twitter_parser.status_user_timeline(twitter_status_user_timeline)
    entry_games = []
    for tweet in tweet_list.get('users'):
        message_tweet = Message(account=account, url='twitter.com', datetime=datetime.datetime.now(),
                           entry_name='text', data=tweet.get('text'),
                           vid=rand_string(), update_date=datetime.datetime.now())
        entry_games.append(message_tweet)
        return_list.append(model_to_dict(message_tweet))
        message_tweet.save()


    pprint('Dynamic Twitter Parser Testing')
    pprint(entry_friends)
    pprint(entry_games)

    return return_list


def parse_facebook():
    facebook_test_mapping = open('../smokesignal/tests/data/facebook/facebook_test_mapping.json', encoding='utf-8').read()
    facebook_me = open('../smokesignal/tests/data/facebook/me.json', encoding='utf-8').read()
    facebook_me_friends = open('../smokesignal/tests/data/facebook/me/friends.json', encoding='utf-8').read()
    facebook_me_inbox = open('../smokesignal/tests/data/facebook/me/inbox.json', encoding='utf-8').read()
    facebook_me_outbox = open('../smokesignal/tests/data/facebook/me/outbox.json', encoding='utf-8').read()
    facebook_parser = Parser.create('facebook', 'facebook', facebook_test_mapping)
    pprint('Dynamic Facebook Parser Testing')
    pprint(facebook_parser.me(facebook_me))
    pprint(facebook_parser.me_friends(facebook_me_friends))
    pprint(facebook_parser.me_inbox(facebook_me_inbox))


def index(request):
    # config = copy.deepcopy(settings.SIGNALS)
    # return HttpResponse(json.dumps(config), content_type='application/json')


    account = Account(name='steam', root_url='')
    account.save()
    parse_steam_response = parse_steam(account)

    return HttpResponse(json.dumps(parse_steam_response), content_type='application/json')
