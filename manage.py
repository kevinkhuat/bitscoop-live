#!/usr/bin/env python
import os
import sys
import django


if __name__ == '__main__':
    DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

    if not DJANGO_SETTINGS_MODULE:
        print('Environment variable DJANGO_SETTINGS_MODULE not found.')
        DJANGO_SETTINGS_MODULE = input('Settings module [ografy.settings.development]: ')

        if not DJANGO_SETTINGS_MODULE:
            DJANGO_SETTINGS_MODULE = 'ografy.settings.development'

        os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
