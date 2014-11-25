from __future__ import unicode_literals

from ografy.lib.smokesignal.parsers import Parser


class Steam(Parser):
    # getplayerSummaries
    # http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids=76561197960435530
    def GetPlayerSummaries(self, json):
        data = self.from_json(json)

        output = {
            'users': []
        }
        players = data.get('players', [])

        for item in players:
            d = {
                'name': item.get('personaname'),
                'lastlogoff': item.get('lastlogoff')
            }
            output['users'].append(d)

        return output

    # GetFriendList
    # http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&steamid=76561197960435530&relationship=friend
    def GetFriendList(self, json):
        data = self.from_json(json)

        output = {
            'users': []
        }
        friends = data.get('friendslist', {}).get('friends', [])

        for item in friends:
            d = {
                'name': item.get('steamid'),
                'friend_since': item.get('friend_since')
            }
            output['users'].append(d)

        return output

    # GetRecentlyPlayedGames
    # http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=1D581D35E86EB4907971BA6CBD05F23F&steamid=76561197960434622&format=json
    def GetRecentlyPlayedGames(self, json):
        data = self.from_json(json)

        output = {
            'games': []
        }
        games = data.get('response', {}).get('games', [])

        for item in games:
            d = {
                'name': item.get('name'),
                'playtime_2weeks': item.get('playtime_2weeks'),
                'playtime_forever': item.get('playtime_forever')
            }
            output['games'].append(d)

        return output
