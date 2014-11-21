from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Lists all users.'

    def handle(self, *args, **options):
        User = get_user_model()

        for user in User.objects.all():
            self.stdout.write('{0}\t{1}'.format(user.email, user.handle))

