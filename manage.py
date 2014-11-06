#!/usr/bin/env python
import os
import sys


if __name__ == '__main__':

    # if os.environ['DJANGO_SETTINGS_MODULE'] is None:
    #     os.environ['DJANGO_SETTINGS_MODULE'] = 'ografy.settings.production'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
