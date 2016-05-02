from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Lists all users with basic information.'

    def handle(self, *args, **options):
        UserModel = get_user_model()
        qs = UserModel.objects.all()

        for user in qs:
            self.stdout.write('{joined}  {name}\t{email}'.format(**{
                'joined': user.date_joined.strftime('%Y/%m/%d'),
                'name': user.full_name or '',
                'email': user.email
            }))
