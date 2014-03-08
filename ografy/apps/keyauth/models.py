from __future__ import unicode_literals
import hmac
import uuid

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError

from ografy.util.decorators import autoconnect

try:
    from hashlib import sha1
except ImportError:
    import sha.sha as sha1


@autoconnect
class Key(models.Model):
    id = models.AutoField(primary_key=True)
    digest = models.CharField(db_index=True, max_length=128)
    whois = models.CharField(max_length=128)
    login_count = models.IntegerField(default=0)
    last_login = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def put_address(self, ip):
        """
        Add an address and pass on any database constraint exceptions.
        """
        address = self.addresses.filter(ip__exact=ip).first()

        if address is None:
            try:
                self.addresses.create(ip=ip)
            except IntegrityError:
                pass
        else:
            # Update the `last_access` field.
            address.save()

    def pre_save(self):
        if not self.digest or self.digest == '':
            self.digest = hmac.new(uuid.uuid4().bytes, digestmod=sha1).hexdigest()


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(db_index=True, max_length=50)  # Long enough for IPv6 and change.
    last_access = models.DateTimeField(null=True, blank=True, auto_now=True, auto_now_add=True)

    key = models.ForeignKey(Key, related_name='addresses')

    class Meta:
        unique_together = ('ip', 'key',)
