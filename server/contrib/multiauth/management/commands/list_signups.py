from django.core.management.base import BaseCommand

from server.contrib.multiauth.models import SignupRequest


class Command(BaseCommand):
    help = 'Lists all signup requests with basic information.'

    def handle(self, *args, **options):
        qs = SignupRequest.objects.all()

        for request in qs:
            self.stdout.write('{date}  {ip}  {email}'.format(**{
                'date': request.date.strftime('%Y/%m/%d'),
                'ip': request.ip,
                'email': request.email
            }))
