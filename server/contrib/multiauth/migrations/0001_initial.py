# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('claimed', models.BooleanField(default=False)),
                ('user_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignupRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=256, unique=True)),
                ('ip', models.CharField(max_length=16)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
