from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<username>'
    help = 'Activates a user.'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('No user identified.')

        username, = args
        user_model = get_user_model()

        try:
            user = user_model._default_manager.get(**{
                user_model.USERNAME_FIELD: username
            })
        except user_model.DoesNotExist:
            raise CommandError('User "{0}" does not exist.'.format(username))

        user.is_active = True
        user.save()

        return 'User "{0}" activated.'.format(username)
