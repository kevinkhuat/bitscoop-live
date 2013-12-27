import xml.etree.ElementTree as Parser
from generic import get_url_content


USERNAME = 'monkisaurus'
PROFILE_URL = 'http://steamcommunity.com/id/{0}/?xml=1'.format(USERNAME)            


def scrape():
    content = get_url_content(PROFILE_URL)
    root = Parser.fromstring(content)
    
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