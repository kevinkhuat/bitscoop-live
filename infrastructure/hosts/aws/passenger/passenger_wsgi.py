import os
import sys


VENV = 'ografy-3.4'
HOME = os.path.expanduser('~')
BASEDIR = os.path.join(HOME, 'environments', VENV)
INTERP = os.path.join(BASEDIR, 'bin', 'python')
CWD = os.getcwd()

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(BASEDIR)
sys.path.append(os.path.join(CWD, 'ografy'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ografy.settings.aws'

import django.core.wsgi
application = django.core.wsgi.get_wsgi_application()
