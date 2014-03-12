import json
from pprint import pprint
from ografy.apps.core.models import Person, Account

class steam_parser:

    def __init__(self):
        pass

    @staticmethod
    def get_player_summary_to_account(self, json_data):
        parsed_data = []
        result = []
        if json_data is not None:
            parsed_data = json.load(json_data)

        #TODO: Needs work where name is not steam id, needs error checking fulshed out
        try:
            if parsed_data["players"] is not None:
                try:
                    for f in parsed_data["players"].items():
                        result.append(Account.objects.create(username=f["personaname"], name="Steam"))
                except ValueError:
                    pass
        except ValueError:
            pass

        return result

    @staticmethod
    def friend_list_to_person(self, json_data):
        parsed_data = []
        result = []
        if json_data is not None:
            parsed_data = json.load(json_data)

        #TODO: Needs work where name is not steam id, needs error checking fulshed out
        try:
            if parsed_data["friendList"]["friends"] is not None:
                try:
                    for f in parsed_data["friendList"]["friends"].items():
                        result.append(Person.objects.create(name=f["steamid"]))
                except ValueError:
                    pass
        except ValueError:
            pass

        return result