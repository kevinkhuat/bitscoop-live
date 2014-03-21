from __future__ import unicode_literals

from django import forms


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput())
