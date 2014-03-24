from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model

from ografy.lib.xauth.fields import PasswordField
from ografy.util.forms import Form, ModelForm


class LoginForm(Form):
    identifier = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)


class SignUpForm(ModelForm):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'handle', 'first_name', 'last_name']
