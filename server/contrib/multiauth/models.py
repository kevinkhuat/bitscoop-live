from django.db import models


class SignupCode(models.Model):
    id = models.AutoField(primary_key=True)
    claimed = models.BooleanField(default=False)
    user_id = models.IntegerField(null=True)


class SignupRequest(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
    ip = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now_add=True)
