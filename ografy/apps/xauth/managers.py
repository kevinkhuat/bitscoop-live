from __future__ import unicode_literals

from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager as BaseManager, Q
from django.utils.timezone import now


class AddressManager(BaseManager):
    def valid(self):
        expression = Q(expires__isnull=True) | Q(expires__gt=now())

        return self.filter(expression)

    def invalid(self):
        return self.filter(expires__lte=now())


class KeyManager(BaseManager):
    def valid(self):
        expression = Q(expires__isnull=True) | Q(expires__gt=now())

        return self.filter(expression)

    def invalid(self):
        return self.filter(expires__lte=now())


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('An email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now(),
                          date_joined=now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def by_oid(self, oid):
        try:
            id = int(oid)
            expr = Q(pk=id)
        except ValueError:
            expr = Q(handle__iexact=oid)

        return self.filter(expr)

    def by_identifier(self, identifier):
        return self.filter(Q(email__iexact=identifier) | Q(handle__iexact=identifier))
