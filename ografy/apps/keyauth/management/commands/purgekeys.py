from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ografy.apps.keyauth.models import Key


class Command(BaseCommand):
    help = 'Removes expired keys from the database.'

    def handle(self, *args, **options):
        count = Key.objects.invalid().count()

        if count > 0:
            Key.objects.invalid().delete()

        self.stdout.write('Removed {0} application keys.'.format(count))
