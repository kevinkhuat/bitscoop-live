import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from ografy.contrib.multiauth.plugins.key.models import Key
from ografy.contrib.pytoolbox.django.datetime import offset


class Command(BaseCommand):
    args = '<username>'
    help = 'Creates an application key for the specified user.'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--seconds', action='store', type=int, dest='seconds',
            help='The number of seconds until the token expires.'
        )

        parser.add_argument('-m', '--minutes', action='store', type=int, dest='minutes',
            help='The number of minutes until the token expires. 60 seconds in 1 minute.'
        )

        parser.add_argument('-r', '--hours', action='store', type=int, dest='hours',
            help='The number of hours until the token expires. 60 minutes in 1 hour.'
        )

        parser.add_argument('-d', '--days', action='store', type=int, dest='days',
            help='The number of days until the token expires. 24 hours in 1 day.'
        )

        parser.add_argument('-w', '--weeks', action='store', type=int, dest='weeks',
            help='The number of weeks until the token expires. 7 days in 1 week.'
        )

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError('Need exactly one or zero arguments for username.')

        if args:
            username, = args
        else:
            username = getpass.getuser()

        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get(**{
                UserModel.USERNAME_FIELD: username
            })
        except UserModel.DoesNotExist:
            raise CommandError('User "{0}" does not exist.'.format(username))

        time_data = {}

        for key in ['seconds', 'minutes', 'hours', 'days', 'weeks']:
            value = options.get(key)
            if value is not None:
                time_data[key] = value

        key = Key(user=user)

        if len(time_data) > 0:
            key.expires = offset(**time_data)

        key.save()

        return 'Application key {0} created for user "{1}".'.format(key.digest, username)
