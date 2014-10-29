import os
import sys


VENV = 'ografy.dev-3.4'
BASEDIR = os.path.join(os.environ['HOME'], 'environments', VENV)
INTERP = os.path.expanduser(os.path.join(BASEDIR, 'bin', 'python'))

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.path.expanduser(BASEDIR))
sys.path.append(os.path.join(os.getcwd(), 'ografy'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ografy.settings.production'

import django.core.wsgi
application = django.core.wsgi.get_wsgi_application()
