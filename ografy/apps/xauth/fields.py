from __future__ import unicode_literals

from django.forms import CharField, PasswordInput

from ografy.apps.xauth.validators import PasswordValidator


class PasswordField(CharField):
    default_validators = [PasswordValidator()]

    def __init__(self, *args, **kwargs):
        if not 'widget' in kwargs:
            kwargs['widget'] = PasswordInput(render_value=False)

        super(PasswordField, self).__init__(*args, **kwargs)
