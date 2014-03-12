import json
from pprint import pprint
from ografy.apps.core.models import Person, Account

class twitter_parser:

    def __init__(self):
        pass

    @staticmethod
    def userlookup_to_account(self, json_data):
        parsed_data = []
        result = []
        if json_data is not None:
            parsed_data = json.load(json_data)

        #TODO: Needs work where name is not steam id, needs error checking fulshed out
        try:
            if parsed_data["players"] is not None:
                try:
                    for f in parsed_data["players"].items():
                        result.append(Account.objects.create(username=f["screen_name"], name=f["name"], root_url=f["url"]))
                except ValueError:
                    pass
        except ValueError:
            pass

        return result

    @staticmethod
    def friends_to_person(self, json_data):
        parsed_data = []
        result = []
        if json_data is not None:
            parsed_data = json.load(json_data)

        #TODO: Needs work where name is not  id, needs error checking fulshed out, pagation issues for large accounts
        try:
            if parsed_data["friends"]["names"] is not None:
                try:
                    for f in parsed_data["friends"]["names"].items():
                        result.append(Person.objects.create(name=f))
                except ValueError:
                    pass
        except ValueError:
            pass

        return result