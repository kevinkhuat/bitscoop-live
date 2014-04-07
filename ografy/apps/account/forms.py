from __future__ import unicode_literals
import re

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from ografy.lib.xauth.fields import PasswordField
from ografy.util.forms import Form


class UpdateDetailsForm(Form):
    """
    We don't want this to be a model form because we can't cut out the "unique" filters selectively.
    We need more control over the validation of `email` and `handle` so that a user can submit their own
    email address and handle without running into errors. I.e. if the user that CAUSES the unique validation
    errors on submit is the request user, then the unique error is unwarranted... but there's no way to tell the
    difference in stock Django.
    """
    email = forms.EmailField(max_length=256)
    handle = forms.CharField(max_length=20, required=False,
        validators=[
            RegexValidator(re.compile(r'^(?=[a-zA-Z0-9_\.]{3,20}$)(?=.*[a-zA-Z])'), _('3-20 letters, numbers, underscores, or periods. Must contain least one letter.'), 'invalid'),
            RegexValidator(re.compile(r'^((?![o0]+[g9]+r+[a4]+(f|ph)+y+).)*$', re.I), _('Username cannot contain Ografy.'), 'invalid'),
        ]
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)


class UpdatePasswordForm(Form):
    password = forms.CharField()
    new_password = PasswordField()
