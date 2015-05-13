import os
import sys

from django.core.wsgi import get_wsgi_application


wd = os.path.dirname(__file__)
lib_path = os.path.join(wd, 'lib')
sys.path.append(os.path.abspath(lib_path))

application = get_wsgi_application()
