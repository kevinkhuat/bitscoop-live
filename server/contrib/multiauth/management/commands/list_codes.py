from django.conf import settings
from django.core.management.base import BaseCommand
from hashids import Hashids as Hasher

from server.contrib.multiauth.models import SignupCode


class Command(BaseCommand):
    help = 'Creates an unclaimed signup code.'

    def handle(self, *args, **options):
        hasher = Hasher(
            min_length=settings.MULTIAUTH_HASH_MINLENGTH,
            salt=settings.MULTIAUTH_HASH_SECRET
        )

        qs = SignupCode.objects.filter(claimed__exact=False).all()

        for code in qs:
            hash = hasher.encode(code.id)
            self.stdout.write('{0}\t{1}'.format(code.id, hash))
