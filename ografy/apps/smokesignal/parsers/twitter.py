from ografy.apps.smokesignal.parsers import Parser


class Twitter(Parser):
    # GET friends/list
    # https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name=twitterapi&skip_status=true&include_user_entities=false
    def friends_list(self, json):
        data = self.from_json(json)

        output = {
            'users': []
        }
        users = data.get('users', [])

        for item in users:
            d = {
                'screen_name': item.get('screen_name'),
                'created_at': item.get('created_at'),
                'description': item.get('description')
            }
            output['users'].append(d)

        return output

    # GET statuses/user_timeline
    # https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2
    def status_user_timeline(self, json):
        data = self.from_json(json)

        output = {
            'tweets': []
        }

        for item in data:
            d = {
                'coordinates': item.get('coordinates'),
                'geo': item.get('geo'),
                'created_at': item.get('created_at'),
                'text': item.get('text')
            }
            output['tweets'].append(d)

        return output
