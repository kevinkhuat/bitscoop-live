from django.conf import settings
from django.core.management.base import BaseCommand
from hashids import Hashids as Hasher

from server.contrib.multiauth.models import SignupCode


class Command(BaseCommand):
    help = 'Lists all usable, outstanding signup codes.'

    def handle(self, *args, **options):
        hasher = Hasher(
            min_length=settings.MULTIAUTH_HASH_MINLENGTH,
            salt=settings.MULTIAUTH_HASH_SECRET
        )

        qs = SignupCode.objects.filter(uses__gt=0).all()

        if options['verbosity'] >= 2:
            self.stdout.write('ID\tHash\tUses\tName')

            for code in qs:
                self.stdout.write('{id}\t{hash}\t{uses}\t{name}'.format(**{
                    'id': code.pk,
                    'hash': hasher.encode(code.id),
                    'uses': code.uses,
                    'name': code.name or ''
                }))
        else:
            for code in qs:
                self.stdout.write(hasher.encode(code.id))
