from __future__ import unicode_literals
import uuid

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User


class Command(BaseCommand):
    args = ''
    help = 'Creates an application key user with an invalid password.'

    def handle(self, *args, **options):
        global input

        try:
            input = raw_input
        except NameError:
            pass

        email = input('Email: ')
        handle = input('Handle: ')
        first_name = input('First Name: ')
        last_name = input('Last Name: ')

        if not email:
            email = '{0}@dummy.ografy.io'.format(uuid.uuid4().hex)

        key_user = User(
            email=email,
            handle=handle,
            first_name=first_name,
            last_name=last_name,
            is_verified=True
        )
        key_user.set_unusable_password()  # Make sure the key user can never log in traditionally.
        key_user.save()

        self.stdout.write('User created.')
