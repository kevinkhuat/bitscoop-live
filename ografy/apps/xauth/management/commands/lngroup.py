from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<user identifier> <group name>'
    help = 'Creates an authentication group.'

    def handle(self, *args, **options):
        if len(args) < 2:
            self.stderr.write('Invalid arguments.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')
            return

        identifier = args[0]
        group_name = args[1]
        User = get_user_model()
        user = User.objects.by_identifier(identifier).first()
        group = Group.objects.filter(name__iexact=group_name).first()

        if user is None:
            self.stderr.write('No user found with identifier "{0}".'.format(identifier))
            return

        if group is None:
            self.stderror.write('No group found with name "{0}".'.format(group_name))
            return

        group.user_set.add(user)
        self.stdout.write('User "{0}" added to group "{1}".'.format(user.identifier, group.name))
