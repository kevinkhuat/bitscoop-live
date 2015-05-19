from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.http import urlquote

from ografy.apps.core.managers import UserManager
from ografy.util.decorators import autoconnect
from ografy.util.fields import NullCharField


@autoconnect
class User(AbstractBaseUser, PermissionsMixin):
    """
    Entity representing a User.

    Attributes:
        id: Entity identifier.
        password: (Inherited) The salted and hashed password value.
        email: Entity-specified email address.
        handle: Entity-specified username.
        first_name: Entity-specified given name.
        last_name: Entity-specified inherited name.
        last_login: The date of last login.
        password_date: The date of the last password change.
        is_verified: Flag indicating whether or not the account has been verified.
        is_active: Flag indicating whether or not the account is active.
    """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    handle = NullCharField(max_length=20, blank=True, null=True, unique=True, db_index=True, validators=settings.HANDLE_VALIDATORS)

    password_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    # Non DBMS-specific case-insensitive unique.
    _upper_email = models.EmailField(max_length=256, blank=True, null=True, unique=True, db_index=True)
    _upper_handle = NullCharField(max_length=20, blank=True, null=True, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    # TODO: Complete for user page.
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    @property
    def is_valid(self):
        return self.is_active and self.is_verified

    @property
    def oid(self):
        return self.handle or self.pk

    @property
    def identifier(self):
        return self.handle or self.email

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.handle or self.first_name

    # TODO: Wire up to email server for email verification and password reset.
    def email_user(self, subject, message, from_email=None):
        pass

    def member_of(self, group_name):
        return self.groups.filter(name__iexact=group_name).exists()

    def pre_save(self):
        self._upper_email = self.email.upper()

        if self.handle is not None:
            self._upper_handle = self.handle.upper()
        else:
            self._upper_handle = self.handle
