import hmac
import uuid
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils import timezone

from ografy.contrib.multiauth.plugins.key.managers import KeyManager
from ografy.contrib.pytoolbox.django.signals import autoconnect


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
