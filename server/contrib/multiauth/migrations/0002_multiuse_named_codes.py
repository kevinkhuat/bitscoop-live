# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def forwards(apps, schema_editor):
    SignupCode = apps.get_model('multiauth', 'signupcode')
    User = apps.get_model('core', 'user')
    db_alias = schema_editor.connection.alias

    for code in SignupCode.objects.using(db_alias).all():
        code.uses = 1 - int(code.claimed)
        code.save()

        try:
            user = User.objects.get(pk=code.user_id)
            code.users.add(user)
        except User.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multiauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupcode',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='+'),
        ),
        migrations.AddField(
            model_name='signupcode',
            name='uses',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='signupcode',
            name='name',
            field=models.CharField(max_length=140, null=True, blank=True),
        ),
        migrations.RunPython(forwards),
        migrations.RemoveField(
            model_name='signupcode',
            name='claimed',
        ),
        migrations.RemoveField(
            model_name='signupcode',
            name='user_id',
        ),
    ]
