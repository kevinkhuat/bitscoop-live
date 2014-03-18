from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ografy.apps.core.models import User


class Command(BaseCommand):
    args = '<user identifier>'
    help = 'Deactivates a user and revokes all keys associated with the account.'

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('No user identified.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')

            return

        identifier = args[0]
        user = User.objects.filter(handle__iexact=identifier).first()
        if user is None:
            user = User.objects.filter(email__iexact=identifier).first()

        if user is not None:
            user.is_active = False
            user.save()

            self.stdout.write('User associated with "{0}" deactivated.'.format(user.email))

            count = user.key_set.valid().count()

            if count > 0:
                user.key_set.update(expires=now())
                self.stdout.write('Revoked {0} application keys.'.format(count))
        else:
            self.stderr.write('User "{0}" does not exist.'.format(identifier))
