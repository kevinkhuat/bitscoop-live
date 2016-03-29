from django.conf import settings
from django.db import models


class SignupCode(models.Model):
    id = models.AutoField(primary_key=True)
    uses = models.IntegerField(default=1)
    name = models.CharField(blank=True, null=True, max_length=140)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')


class SignupRequest(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    ip = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now_add=True)
