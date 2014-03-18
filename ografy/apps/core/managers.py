from __future__ import unicode_literals

from django.contrib.auth.models import BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('An email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def by_identifier(self, email=None, handle=None, both=None):
        if both is not None:
            expr = Q(email__iexact=both) | Q(handle__iexact=both)
        elif email is not None:
            expr = Q(email__iexact=email)
        elif handle is not None:
            expr = Q(handle__iexact=handle)
        else:
            expr = Q()

        return self.filter(expr)
