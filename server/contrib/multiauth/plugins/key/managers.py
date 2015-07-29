from django.db.models import Manager as BaseManager, Q
from django.utils.timezone import now


class KeyManager(BaseManager):
    def valid(self):
        expression = Q(expires__isnull=True) | Q(expires__gt=now())

        return self.filter(expression)

    def invalid(self):
        return self.filter(expires__lte=now())
