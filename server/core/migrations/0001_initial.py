# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import django.core.validators
from django.db import migrations, models

import server.contrib.pytoolbox.django.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(db_index=True, unique=True, max_length=256)),
                ('handle', server.contrib.pytoolbox.django.fields.NullCharField(unique=True, blank=True, validators=[django.core.validators.RegexValidator(re.compile('^(?=[a-zA-Z0-9_\\.]{3,20}$)(?=.*[a-zA-Z])', 32), '3-20 letters, numbers, underscores, or periods. Must contain at least one letter.'), django.core.validators.RegexValidator(re.compile('[b]+[i1\\|]+[t7]+[s5]+[c]+[o0]+[p]*', 34), 'Username cannot contain BitScoop.', inverse_match=True)], max_length=20, null=True, db_index=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('gender', models.CharField(blank=True, null=True, max_length=30)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('_upper_email', models.EmailField(blank=True, db_index=True, unique=True, null=True, max_length=256)),
                ('_upper_handle', server.contrib.pytoolbox.django.fields.NullCharField(blank=True, db_index=True, unique=True, null=True, max_length=20)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', blank=True, related_name='user_set', to='auth.Group', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', blank=True, related_name='user_set', to='auth.Permission', related_query_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
