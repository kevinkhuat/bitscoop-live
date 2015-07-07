from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now

from ografy.contrib.multiauth.plugins.key.models import Key


class Command(BaseCommand):
    help = 'Revokes keys matching provided conditions.'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--key', action='store', dest='key',
            help='Limit the key revocation set to a specific digest.'
        )

        parser.add_argument('-u', '--user', action='store', dest='user',
            help='Limit the key revocation set to a specific user. '
        )

    def handle(self, *args, **options):
        filter_expr = Q()
        limited = False

        if options.get('key') is not None:
            filter_expr &= Q(digest__exact=options.get('key'))
            limited = True

        if options.get('user') is not None:
            user_model = get_user_model()
            filter_expr &= Q(**{
                'user__{0}__iexact'.format(user_model.USERNAME_FIELD): options.get('user')
            })
            limited = True

        key_set = Key.objects.valid().filter(filter_expr)
        count = key_set.count()

        if count > 0:
            if not limited:
                self.stdout.write('You have not limited the range of keys that will be invalidated.')
                self.stdout.write('This action will apply to all keys.')

                confirm = input('Are you sure you want to do this? (yes/no):')

                while 1:
                    if confirm not in ('yes', 'no'):
                        confirm = input('Please enter either "yes" or "no": ')
                        continue

                    if confirm == 'yes':
                        break
                    else:
                        return 'Command cancelled, no changes made.'

            key_set.update(expires=now())

            return 'Revoked {0} application keys.'.format(count)
        else:
            return 'No active application keys found.'
