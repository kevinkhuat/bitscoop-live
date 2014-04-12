import xml.etree.ElementTree as etree

from smokesignal.signals import Signal


class Steam(Signal):
    def __init__(self, username):
        url = 'http://steamcommunity.com/id/{0}/?xml=1'.format(username)
        super(Steam, self).__init__(url)

    def scrape(self):
        content = super(Steam, self).scrape()

        if content is None:
            return None

        root = etree.fromstring(content)
        online_state = root.find('onlineState').text
        total_hours = float(root.find('hoursPlayed2Wk').text)

        data = {
            'online_state': online_state,
            'total_hours': total_hours,
            'games': []
        }

        for game in root.iter('mostPlayedGame'):
            name = game.find('gameName').text
            steam_url = game.find('gameLink').text
            icon_url = game.find('gameIcon').text
            game_hours = float(game.find('hoursPlayed').text)

            if game_hours > 0.1 * total_hours:
                g = {
                    'name': name,
                    'steam_url': steam_url,
                    'icon_url': icon_url,
                    'game_hours': game_hours
                }
                data['games'].append(g)

        return data
