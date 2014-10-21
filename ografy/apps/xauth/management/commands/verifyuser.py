from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<user identifier>'
    help = 'Manually verifies a user by setting the `is_verified` flag to `True`.'

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('No user identified.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')
            raise Exception

        identifier = args[0]
        User = get_user_model()
        user = User.objects.by_identifier(identifier).first()

        if user is not None:
            user.is_active = True
            user.is_verified = True
            user.save()

            self.stdout.write('User associated with "{0}" verified.'.format(user.email))
        else:
            self.stderr.write('User "{0}" does not exist.'.format(identifier))
