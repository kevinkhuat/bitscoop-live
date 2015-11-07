from django import forms
from django.forms import Form


class LoginForm(Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
