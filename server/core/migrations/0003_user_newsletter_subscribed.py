# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_insert_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='newsletter_subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
