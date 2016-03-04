# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_demo_user(apps, *args):
    UserModel = apps.get_model('core', 'User')

    user = UserModel(
        handle='biffs',
        email='biff.scoops@bitscoop.com',
        last_name='Scoops',
        first_name='Biff',
        password='pbkdf2_sha256$20000$KUU2YGvoR33F$zuEM1GZu6LHMT6UWcjoVbSzh/j0fU1f3zL/ibuL1WNc='
    )

    # user.set_password('foxtrot1234')
    user.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_demo_user),
    ]
