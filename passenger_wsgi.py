import os
import sys


CWD = os.getcwd()
ROOT = os.path.abspath(os.sep)
VENV = os.path.join(ROOT, 'var', 'lib', 'ografy', 'environments', 'ografy-3.4')
INTERP = os.path.join(VENV, 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(VENV)
sys.path.append(os.path.join(CWD, 'ografy'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ografy.settings.production')

from ografy.wsgi import application