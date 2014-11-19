#!/usr/bin/env python
import os
import sys


if __name__ == '__main__':

    #if 'DJANGO_SETTINGS_MODULE' in os.environ:
    #    os.environ['DJANGO_SETTINGS_MODULE'] = 'ografy.settings.development'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
