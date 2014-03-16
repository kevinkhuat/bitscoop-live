from __future__ import unicode_literals
import hmac
import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from ografy.lib.auth.managers import AddressManager, KeyManager

try:
    from hashlib import sha1
except ImportError:
    import sha.sha as sha1


class Key(models.Model):
    id = models.AutoField(primary_key=True)
    digest = models.CharField(db_index=True, unique=True, max_length=128)
    expires = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = KeyManager()

    def __init__(self, *args, **kwargs):
        kwargs.pop('digest', None)
        super(Key, self).__init__(*args, **kwargs)
        self.digest = hmac.new(uuid.uuid4().bytes, digestmod=sha1).hexdigest()

    @property
    def is_valid(self):
        return self.expires is None or self.expires > now()


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
        return self.is_verified and (self.expires is None or self.expires > now())

    def flag_access(self):
        self.last_access = now()
        self.save()

    class Meta:
        unique_together = ('ip', 'user',)
