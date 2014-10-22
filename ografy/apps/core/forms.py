from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from ografy.apps.xauth.fields import PasswordField
from django.forms import ModelForm


class SignUpForm(ModelForm):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'handle', 'first_name', 'last_name']
