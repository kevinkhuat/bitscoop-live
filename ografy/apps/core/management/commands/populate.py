import random
import string

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User, Entry


BANK = string.ascii_uppercase + string.ascii_lowercase + string.digits


def rand_string(length=15):
    return ''.join(random.choice(BANK) for x in range(length))


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for n in range(100):
            user = User(first_name=rand_string(), last_name=rand_string(), email=rand_string())
            user.save()

            fb = user.account_set.create(name='Facebook')
            t = user.account_set.create(name='Twitter')
            mint = user.account_set.create(name='Mint')

            entries = []
            for n in range(100):
                entries.append(Entry(
                    account=fb,
                    data=rand_string(50)
                ))
            Entry.objects.bulk_create(entries)

            entries = []
            for n in range(100):
                entries.append(Entry(
                    account=t,
                    data=rand_string(50)
                ))
            Entry.objects.bulk_create(entries)

            entries = []
            for n in range(100):
                entries.append(Entry(
                    account=mint,
                    data=rand_string(50)
                ))
            Entry.objects.bulk_create(entries)