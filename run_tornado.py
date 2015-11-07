import sys

import django
import tornado.web
import tornado.wsgi
from tornado.ioloop import IOLoop

from server.apps.passthrough.routes import patterns


# This module starts a Tornado server on a certain port.
# By default this is port 8001, but you can pass any port in as a parameter when calling the script.
# e.g. `python run_tornado.py 8005` to start Tornado on port 8005
if __name__ == '__main__':
    port = 8001

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    # Django session information is used to authenticate the user making requests to the Tornado server
    # django.setup needs to be run to initialize the models used for sessions.
    django.setup()

    application = tornado.web.Application(patterns)

    print('Starting HTTP proxy...')  # noqa

    application.listen(port, address='127.0.0.1')

    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()

    print('Application listening on port %d...' % port)  # noqa
