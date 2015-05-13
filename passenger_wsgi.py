import os
import sys


ROOT = os.path.abspath(os.sep)
VENV = os.path.join(ROOT, 'var', 'lib', 'ografy', 'environments', 'ografy-3.4')
INTERP = os.path.join(VENV, 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(VENV)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ografy.settings.production')

from ografy.wsgi import application
