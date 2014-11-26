from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<name>'
    help = 'Creates an authentication group.'

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('No name provided.')
            self.stderr.write('Use the --help flag to view appropriate uses for this command.')
            return

        name = args[0]
        group = Group.objects.filter(name__iexact=name).first()

        if group is None:
            group = Group(name=name)
            group.save()
            self.stdout.write('Group "{0}" created.'.format(name))
        else:
            self.stderr.write('Group "{0}" already exists. No changes made.'.format(group.name))
