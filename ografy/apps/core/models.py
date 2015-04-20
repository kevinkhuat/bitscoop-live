from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.http import urlquote

from ografy.apps.core.managers import UserManager
from ografy.util.decorators import autoconnect
from ografy.util.fields import NullCharField


class Provider(models.Model):
    """
    Entity representing a Provider.

    Attributes:
        id: A unique database descriptor set in the fixture.
        name: The name of the linked service.
        backend_name: The name of the linked service according to PSA backend library.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    backend_name = models.CharField(max_length=250)
    auth_backend = models.CharField(max_length=250)
    description = models.CharField(max_length=2500)
    tags = models.CharField(max_length=1000)

    def __str__(self):
        return '{0} {1}'.format(self.id, self.backend_name)


class Signal(models.Model):
    """
    Entity representing an integrated Signal.

    Attributes:
        id: A unique database descriptor obtained when saving a Signal.
        user: A foreign key relationship to the User entity who owns the Signal.
        name: The name of the linked service.
    """
    FREQUENCY = (
        (0, 'Premium On Demand'),
        (1, 'Daily'),
        (2, 'Weekly'),
        (3, 'Manual'),
        (4, 'Once'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    provider = models.ForeignKey(Provider)
    name = models.CharField(max_length=100)
    psa_backend_uid = models.CharField(max_length=100)

    complete = models.BooleanField(default=False)
    connected = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)

    frequency = models.PositiveSmallIntegerField(default=1, choices=FREQUENCY)

    created = models.DateTimeField(blank=False)
    updated = models.DateTimeField(blank=False)

    access_token = models.CharField(max_length=100)
    oauth_token = models.CharField(max_length=100)

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.id, self.name, self.provider, self.user.handle)


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

class permissionTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    url = models.CharField(max_length = 100, blank=False)
    provider = models.ForeignKey(Provider)
    enabled_by_default = models.BooleanField(default=True)

class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    url = models.CharField(max_length = 100, blank=False)
    provider = models.ForeignKey(Provider)
    enabled = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    template = models.ForeignKey(permissionTemplate)
    signal = models.ForeignKey(Signal)
