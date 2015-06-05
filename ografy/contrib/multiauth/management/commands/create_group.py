from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<name>'
    help = 'Creates an authentication group.'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No group name provided.')

        name, = args

        group = Group.objects.filter(name__iexact=name).first()

        if group is None:
            group = Group(name=name)
            group.save()

            return 'Group "{0}" created.'.format(name)
        else:
            raise CommandError('Group "{0}" already exists.'.format(name))
