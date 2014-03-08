from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User
from ografy.apps.keyauth.models import Key


class Command(BaseCommand):
    args = '<whois>'
    help = 'Creates an application key for the specified user name.'

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('Whois not specified.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')
            return

        whois = args[0]
        key_user = User.objects.filter(email='key.user@ografy.io').first()

        if not key_user:
            key_user = User(
                email='key.user@ografy.io',
                first_name='Key',
                last_name='User',
                is_verified=True
            )
            key_user.set_unusable_password()  # Make sure the key user can never log in traditionally.
            key_user.save()

        key = Key(
            whois=whois,
            user=key_user
        )
        key.save()

        self.stdout.write('Application key {0} created for "{1}".'.format(key.digest, whois))
