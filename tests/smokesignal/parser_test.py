from ografy.lib.smokesignal.parsers import Parser

from pprint import pprint


steam_test_mapping = open('data/steam/steam_test_mapping.json', encoding='utf-8').read()
twitter_test_mapping = open('data/twitter/twitter_test_mapping.json', encoding='utf-8').read()
facebook_test_mapping = open('data/facebook/facebook_test_mapping.json', encoding='utf-8').read()

steam_GetFriendList = open('data/steam/GetFriendList.json', encoding='utf-8').read()
steam_GetPlayerSummaries = open('data/steam/GetPlayerSummaries.json', encoding='utf-8').read()
steam_GetRecentlyPlayedGames = open('data/steam/GetRecentlyPlayedGames.json', encoding='utf-8').read()

twitter_friends_List = open('data/twitter/friends/list.json', encoding='utf-8').read()
twitter_status_user_timeline = open('data/twitter/status/user_timeline.json', encoding='utf-8').read()

facebook_me = open('data/facebook/me.json', encoding='utf-8').read()
facebook_me_friends = open('data/facebook/me/friends.json', encoding='utf-8').read()
facebook_me_inbox = open('data/facebook/me/inbox.json', encoding='utf-8').read()
facebook_me_outbox = open('data/facebook/me/outbox.json', encoding='utf-8').read()

steam_parser = Parser.create("Steam", "Steam", steam_test_mapping)
twitter_parser = Parser.create("Twitter", "Twitter", twitter_test_mapping)
facebook_parser = Parser.create("facebook", "facebook", facebook_test_mapping)

pprint("Dynamic Steam Parser Testing")
pprint(steam_parser.GetPlayerSummaries(steam_GetPlayerSummaries))
pprint(steam_parser.GetFriendList(steam_GetFriendList))
pprint(steam_parser.GetRecentlyPlayedGames(steam_GetRecentlyPlayedGames))

pprint("Dynamic Twitter Parser Testing")
pprint(twitter_parser.friends_list(twitter_friends_List))
pprint(twitter_parser.status_user_timeline(twitter_status_user_timeline))

pprint("Dynamic Facebook Parser Testing")
pprint(facebook_parser.me(facebook_me))
pprint(facebook_parser.me_friends(facebook_me_friends))
pprint(facebook_parser.me_inbox(facebook_me_inbox))
# pprint(facebook_parser.me_outbox(facebook_me_outbox))
