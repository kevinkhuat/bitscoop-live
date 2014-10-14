from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from example.app.models import Account

class AccountCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(AccountCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = Account
        fields = ("email",)

class AccountChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(AccountChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = Account