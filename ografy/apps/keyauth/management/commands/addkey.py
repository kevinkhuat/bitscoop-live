from __future__ import unicode_literals
from optparse import make_option

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User
from ografy.apps.keyauth.models import Key


class Command(BaseCommand):
    args = '<email address>'
    help = 'Creates an application key for the specified user name.'
    option_list = BaseCommand.option_list + (
        make_option(
            '-e',
            '--expires',
            action='store',
            type='int',
            dest='expires',
            help='The number of seconds until the token expires. If unspecified the token will not expire unless explicitly revoked.'
        ),
    )

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('Email address not specified.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')

            return

        email = args[0]
        user = User.objects.filter(email=email).first()

        if user is not None:
            key = Key(user=user)
            key.set_expiration(options.get('expires'))
            key.save()

            self.stdout.write('Application key {0} created for "{1}".'.format(key.digest, user.email))
        else:
            self.stderr.write('User "{0}" does not exist. No application key added.'.format(email))
