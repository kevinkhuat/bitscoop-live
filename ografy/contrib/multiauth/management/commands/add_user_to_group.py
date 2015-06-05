from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<username> <group name>'
    help = 'Adds a user to an authentication group.'

    def handle(self, *args, **options):
        if len(args) < 2:
            self.stderr.write('Invalid arguments.')
            return

        username, group_name, = args

        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get(**{
                UserModel.USERNAME_FIELD: username
            })
        except UserModel.DoesNotExist:
            raise CommandError('User "{0}" does not exist.'.format(username))

        try:
            group = Group.objects.get(**{
                'name__iexact': group_name
            })
        except Group.DoesNotExist:
            raise CommandError('Group "{0}" does not exist.'.format(group_name))

        group.user_set.add(user)

        return 'User "{0}" added to group "{1}".'.format(username, group_name)
