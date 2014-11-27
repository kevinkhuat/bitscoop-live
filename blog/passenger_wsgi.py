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
sys.path.append(os.path.join(CWD))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

from ografy.wsgi import application
