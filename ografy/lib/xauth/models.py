from __future__ import unicode_literals
import hmac
import re
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from ografy.lib.xauth.managers import AddressManager, KeyManager, UserManager
from ografy.util.decorators import autoconnect
from ografy.util.fields import NullCharField

try:
    from hashlib import sha1
except ImportError:
    import sha.sha as sha1

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
    email = models.EmailField(_('email address'), max_length=256, unique=True, db_index=True)
    handle = NullCharField(
        max_length=20, blank=True, null=True, unique=True, db_index=True,
        help_text=_('Required. 3-20 characters. Letters, numbers, underscore and periods permitted. At least one letter.'),
        validators=[
            RegexValidator(re.compile(r'^(?=[a-zA-Z0-9_\.]{3,20}$)(?=.*[a-zA-Z])'), _('3-20 letters, numbers, underscores, or periods. Must contain least one letter.'), 'invalid'),
            RegexValidator(re.compile(r'^((?![o0]+[g9]+r+[a4]+(f|ph)+y+).)*$', re.I), _('Username cannot contain Ografy.'), 'invalid'),
        ]
    )

    password_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, auto_now_add=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_verified = models.BooleanField(_('verified'), default=False)

    _upper_email = models.EmailField(max_length=256, blank=True, null=True, unique=True, db_index=True)  # Non DBMS-specific case-insensitive unique.
    _upper_handle = NullCharField(max_length=20, blank=True, null=True, unique=True, db_index=True)  # Non DBMS-specific case-insensitive unique.

    USERNAME_FIELD = 'email'
    objects = UserManager()

    #Todo: Flush out for user page
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

    #Todo: wire up to email server for email verification and password reset
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


@autoconnect
class Key(models.Model):
    id = models.AutoField(primary_key=True)
    digest = models.CharField(db_index=True, unique=True, max_length=128)
    expires = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = KeyManager()

    @property
    def is_valid(self):
        return self.expires is None or self.expires > timezone.now()

    def pre_save(self):
        if not self.digest:
            self.digest = hmac.new(uuid.uuid4().bytes, digestmod=sha1).hexdigest()


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(db_index=True, max_length=50)  # Long enough for IPv6 and change.
    last_access = models.DateTimeField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)
    _is_verified = models.BooleanField(db_column='is_verified', default=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = AddressManager()

    # Dummy property for the time being. We track IP addresses, but we don't have any way to verify them yet.
    # We won't bother offering this service for key users, but will turn this feature on for regular users at release.
    @property
    def is_verified(self):
        return True

    @property
    def is_valid(self):
        return self.is_verified and (self.expires is None or self.expires > timezone.now())

    def flag_access(self):
        self.last_access = timezone.now()
        self.save()

    class Meta:
        unique_together = ('ip', 'user',)
