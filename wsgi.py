import os
import sys

from django.core.wsgi import get_wsgi_application


wd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(wd, 'lib')))

application = get_wsgi_application()
