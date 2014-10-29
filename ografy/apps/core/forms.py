from __future__ import unicode_literals

# from django.contrib.auth import get_user_model
from ografy.apps.xauth.models import User

from ografy.apps.xauth.fields import PasswordField
from django.forms import ModelForm


class SignUpForm(ModelForm):
    password = PasswordField()

    class Meta:
        # FIXME: Known 1.7 bug
        # model = get_user_model()
        model = User
        fields = ['email', 'handle', 'first_name', 'last_name']
