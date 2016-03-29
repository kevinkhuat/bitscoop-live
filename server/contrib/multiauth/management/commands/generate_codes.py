from django.conf import settings
from django.core.management.base import BaseCommand
from hashids import Hashids as Hasher

from server.contrib.multiauth.models import SignupCode


class Command(BaseCommand):
    help = 'Creates an unclaimed signup code.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            '-n',
            type=int,
            dest='count',
            default=1,
            help='Number of signup codes to generate.'
        )

        parser.add_argument(
            '--uses',
            type=int,
            dest='uses',
            default=1,
            help='Number of uses for the signup code.'
        )

        parser.add_argument(
            '--name',
            type=str,
            dest='name',
            help='The name for the signup code'
        )

        parser.add_argument(
            '--min-length',
            type=int,
            dest='min_length',
            default=settings.MULTIAUTH_HASH_MINLENGTH,
            help='Minimum length of signup code(s).'
        )

        parser.add_argument(
            '--salt',
            dest='salt',
            default=settings.MULTIAUTH_HASH_SECRET,
            help='Minimum length of signup code(s).'
        )

        parser.add_argument(
            '--dry-run',
            '-d',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Generate signup codes without saving to the database.'
        )

        parser.add_argument(
            '--start',
            dest='start',
            type=int,
            default=0,
            help='Starting position of the dry-run. Has no effect if not executing a dry-run.'
        )

    def handle(self, *args, **options):
        hasher = Hasher(
            min_length=options['min_length'],
            salt=options['salt']
        )

        if options['dry_run']:
            for n in range(options['start'], options['start'] + options['count']):
                hash = hasher.encode(n + 1)

                self.stdout.write('{0}\t{1}'.format(n + 1, hash))
        else:
            for n in range(options['count']):
                code = SignupCode(
                    uses=options['uses'],
                    name=options['name']
                )
                code.save()

                hash = hasher.encode(code.id)

                self.stdout.write(hash)
