import getpass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_str

from server.core.api import SettingsApi
from server.core.validators import PasswordValidator


class Command(BaseCommand):
    help = 'Create a new BitScoop user and a related Settings object.'
    requires_system_checks = False

    def _get_text(self, prompt='Handle: '):
        text = input(prompt)

        if not text:
            raise CommandError('aborted')

        return text

    def _get_pass(self, prompt='Password: '):
        p = getpass.getpass(prompt=force_str(prompt))

        if not p:
            raise CommandError('aborted')

        return p

    def handle(self, *args, **options):
        handle_valid = False

        while not handle_valid:
            errors = []
            handle = self._get_text(prompt='Handle: ')

            for v in settings.HANDLE_VALIDATORS:
                try:
                    v(handle)
                except exceptions.ValidationError as e:
                    errors.extend(e.error_list)

            if errors:
                self.stderr.write(errors)
            else:
                handle_valid = True

        email = self._get_text(prompt='Email: ')
        first_name = self._get_text('First name: ')
        last_name = self._get_text('Last name: ')
        password_valid = False

        while not password_valid:
            password = self._get_pass()

            try:
                PasswordValidator().__call__(password)
                password_valid = True
            except exceptions.ValidationError as e:
                self.stderr.write(e.error_list)

        user_model = get_user_model()
        new_user = user_model(handle=handle, email=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        SettingsApi.post({'user_id': new_user.id})

        return 'Successfully created user "%s"' % new_user
