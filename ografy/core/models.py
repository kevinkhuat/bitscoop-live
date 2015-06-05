from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ografy.contrib.pytoolbox.django.fields import NullCharField
from ografy.contrib.pytoolbox.django.signals import autoconnect
from ografy.core.managers import UserManager


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
        date_joined: The date the user joined.
        last_login: (Inherited) The date of last login.
        is_staff: Flag indicating whether or not the account as access to the built-in Django admin app.
        is_active: Flag indicating whether or not the account is active.
    """
    id = models.AutoField(primary_key=True)
    # password = models.CharField(max_length=128)  # Inherited from AbstractBaseUser.
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    handle = NullCharField(max_length=20, blank=True, null=True, unique=True, db_index=True, validators=settings.HANDLE_VALIDATORS)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(blank=True, null=True)  # Inherited from AbstractBaseUser.

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)  # Inherited from PermissionsMixin

    # groups = models.ManyToManyField(Group, blank=True)  # Inherited from PermissionsMixin
    # user_permissions = models.ManyToManyField(Permission, blank=True)  # Inherited from PermissionsMixin

    # Non DBMS-specific case-insensitive unique.
    # These fields are set with a pre-save signal, are intrinsically related to actual model fields,
    # and should not be directly modified.
    _upper_email = models.EmailField(max_length=256, blank=True, null=True, unique=True, db_index=True)
    _upper_handle = NullCharField(max_length=20, blank=True, null=True, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    @property
    def identifier(self):
        return self.handle or self.email

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name).strip()

    @property
    def short_name(self):
        return self.handle or self.first_name

    # Requisite implementation of inherited abstract method.
    def get_full_name(self):
        return self.full_name

    # Requisite implementation of inherited abstract method.
    def get_short_name(self):
        return self.short_name

    def member_of(self, group_name):
        return self.groups.filter(name__iexact=group_name).exists()

    def pre_save(self):
        self._upper_email = self.email.upper()

        if self.handle:
            self._upper_handle = self.handle.upper()
