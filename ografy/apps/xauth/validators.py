from __future__ import unicode_literals
import re
import six

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


PASSWORD_REGEXP = getattr(settings, 'PASSWORD_REGEXP', r'^(?=\w{6,15}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)')
INVALID_PASSWORD_MESSAGE = getattr(settings, 'INVALID_PASSWORD_MESSAGE', 'Invalid password.')


class PasswordValidator(object):
    message = _(INVALID_PASSWORD_MESSAGE)
    code = 'invalid'

    def __init__(self, regex=PASSWORD_REGEXP, message=INVALID_PASSWORD_MESSAGE, code='invalid'):
        self.regex = regex
        self.message = message
        self.code = code

        # Compile the regex if it was not passed pre-compiled.
        if isinstance(self.regex, six.string_types):
            self.regex = re.compile(self.regex)

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if not self.regex.search(force_text(value)):
            raise ValidationError(self.message, code=self.code)
