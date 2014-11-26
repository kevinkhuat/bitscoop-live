from optparse import make_option

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ografy.apps.xauth.models import Key
from ografy.util.datetime import offset


class Command(BaseCommand):
    args = '<user identifier>'
    help = 'Creates an application key for the specified user.'
    opts = (
        make_option(
            '-s',
            '--seconds',
            action='store',
            type='int',
            dest='seconds',
            help='The number of seconds until the token expires.'
        ),

        make_option(
            '-m',
            '--minutes',
            action='store',
            type='int',
            dest='minutes',
            help='The number of minutes until the token expires. 60 seconds in 1 minute.'
        ),

        make_option(
            '-r',
            '--hours',
            action='store',
            type='int',
            dest='hours',
            help='The number of hours until the token expires. 60 minutes in 1 hour.'
        ),

        make_option(
            '-d',
            '--days',
            action='store',
            type='int',
            dest='days',
            help='The number of days until the token expires. 24 hours in 1 day.'
        ),

        make_option(
            '-w',
            '--weeks',
            action='store',
            type='int',
            dest='weeks',
            help='The number of weeks until the token expires. 7 days in 1 week.'
        ),
    )
    option_list = BaseCommand.option_list + opts

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('No user identified.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')

            return

        identifier = args[0]
        User = get_user_model()
        user = User.objects.by_identifier(identifier).first()

        if user is not None:
            time_data = {}
            for key in ['seconds', 'minutes', 'hours', 'days', 'weeks']:
                value = options.get(key)
                if value is not None:
                    time_data[key] = value

            key = Key(user=user)
            if len(time_data) > 0:
                key.expires = offset(**time_data)
            key.save()

            self.stdout.write('Application key {0} created for "{1}".'.format(key.digest, user.identifier))
        else:
            self.stderr.write('User "{0}" does not exist. No application key added.'.format(identifier))
