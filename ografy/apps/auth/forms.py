from __future__ import unicode_literals

from django import forms

from ografy.util.forms import Form


class LoginForm(Form):
    identifier = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
