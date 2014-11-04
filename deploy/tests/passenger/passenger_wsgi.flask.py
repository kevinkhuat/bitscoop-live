import os
import sys

VENV = 'ografy.flask-3.4'
HOME = os.path.expanduser(os.environ['HOME'])
BASEDIR = os.path.join(HOME, 'environments', VENV)
INTERP = os.path.join(BASEDIR, 'bin', 'python')


if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(BASEDIR)
sys.path.append(os.path.join(os.getcwd(),'ografy'))

from ografy.settings.test import name

print(INTERP)
print(sys.path)
print(name)

from flask import Flask
application = Flask(__name__)

@application.route('/')
def index():
    return 'Hello, world! Smell my farts ' + name