import re

from django import forms
from django.core.validators import RegexValidator
from django.forms import Form, ModelForm
from django.utils.translation import ugettext_lazy as _

from ografy.core.documents import Location, Signal
from ografy.core.fields import PasswordField
from ografy.core.models import User


class LoginForm(Form):
    identifier = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)


class SignUpForm(ModelForm):
    password = PasswordField()

    class Meta:
        # FIXME: Known 1.7 bug
        # model = get_user_model()
        model = User
        fields = ['email', 'handle', 'first_name', 'last_name']


class UpdateLocationForm(Form):
    LOCATION_ESTIMATION_METHOD = Location.LOCATION_ESTIMATION_METHOD

    allow_location_collection = forms.BooleanField(required=False)
    location_estimation_method = forms.ChoiceField(choices=LOCATION_ESTIMATION_METHOD, required=False)


class UpdateSignalForm(Form):
    FREQUENCY = Signal.FREQUENCY

    frequency = forms.ChoiceField(choices=FREQUENCY, required=False)


class UpdateAccountForm(Form):
    """
    We don't want this to be a model form because we can't cut out the "unique" filters selectively.
    We need more control over the validation of `email` and `handle` so that a user can submit their own
    email address and handle without running into errors. I.e. if the user that CAUSES the unique validation
    errors on submit is the request user, then the unique error is unwarranted... but there's no way to tell the
    difference in stock Django.
    """
    email = forms.EmailField(max_length=256, required=False)
    handle = forms.CharField(
        max_length=20,
        required=False,
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
