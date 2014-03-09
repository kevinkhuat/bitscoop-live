from __future__ import unicode_literals

from django.db.models import Manager as BaseManager, Q
from django.utils.timezone import now


class KeyManager(BaseManager):
    def valid(self):
        time = now()
        expression = Q(expires__gt=time) | Q(expires__isnull=True)

        return self.filter(expression)

    def invalid(self):
        time = now()

        return self.filter(expires__lte=time)
