from hashlib import sha1
import hmac
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from ografy.apps.xauth.managers import AddressManager, KeyManager
from ografy.util.decorators import autoconnect



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
