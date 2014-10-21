from __future__ import unicode_literals
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from ografy.apps.xauth.models import Key


class Command(BaseCommand):
    help = 'Revokes keys matching provided conditions.'
    opts = (
        make_option(
            '-k',
            '--key',
            action='store',
            dest='key',
            help='Limit the key revocation set to a specific digest.'
        ),

        make_option(
            '-u',
            '--user',
            action='store',
            dest='user',
            help='Limit the key revocation set to a specific user. '
        ),
    )
    option_list = BaseCommand.option_list + opts

    def handle(self, *args, **options):
        filter_expr = Q()

        if options.get('key') is not None:
            filter_expr &= Q(digest__exact=options.get('key'))

        if options.get('user') is not None:
            filter_expr &= Q(user__email__iexact=options.get('user')) | Q(user__handle__iexact=options.get('user'))

        key_set = Key.objects.valid().filter(filter_expr)
        count = key_set.count()

        if count > 0:
            key_set.update(expires=now())
            self.stdout.write('Revoked {0} application keys.'.format(count))
        else:
            self.stdout.write('No application keys found matching the specified criteria.')
