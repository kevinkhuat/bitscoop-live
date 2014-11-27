import uuid

from django.conf import settings
from django.db import models

# TODO: Add fixtures for PSA providers


class Signal(models.Model):
    """
    Entity representing an integrated Signal.

    Attributes:
        id: A unique database descriptor obtained when saving a Signal.
        user: A foreign key relationship to the User entity who owns the Signal.
        name: The name of the linked service.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    provider = models.ForeignKey('Provider')
    name = models.CharField(max_length=50)

    # TODO: FIX
    PSA_A_ID = ''
    PSA_USA_ID = ''

    def __unicode__(self):
        return u'<SIGNAL_{0}: {1}@{2}>'.format(self.id, self.user.display_name, self.name)


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
    backend_name = models.CharField(max_length=150)

    def __unicode__(self):
        return u'<PROVIDER_{0}: {1}@{2}>'.format(self.id, self.name, self.backend_name)


