import random
import string

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User


BANK = string.ascii_uppercase + string.ascii_lowercase + string.digits


def rand_string(length=15):
    return ''.join(random.choice(BANK) for x in range(length))


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User(name="Test")
        user.save()

        for n in range(100):
            user.entry_set.create(data=rand_string())