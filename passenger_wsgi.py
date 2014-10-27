import os
import sys


# VENV = 'ografy_env'
# BASEDIR = os.path.join(os.environ['HOME'], 'bin', 'python27', 'environments', VENV)
# INTERP = os.path.expanduser(os.path.join(BASEDIR, 'bin', 'python'))

BASEDIR = '/ografy/ografy_env/'
INTERP = '/ografy/ografy_env/bin/python3.4'

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.path.expanduser(BASEDIR))
sys.path.append(os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = 'ografy.settings.production'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
