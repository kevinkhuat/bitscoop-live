import json
import sys

import django
import tornado.web
import tornado.wsgi
from tornado import gen
from tornado.ioloop import IOLoop

from ografy.apps.passthrough.api.handler import es_connection
from ografy.apps.passthrough.routes import patterns
from ografy.contrib.estoolbox import (
    CONTACT_MAPPING, CONTENT_MAPPING, DATA_MAPPING, EVENT_MAPPING, LOCATION_MAPPING, SEARCH_MAPPING
)


# This module starts a Tornado server on a certain port.
# By default this is port 8001, but you can pass any port in as a parameter when calling the script.
# e.g. `python run_tornado.py 8005` to start Tornado on port 8005

@gen.coroutine
def put_mappings():
    es_connection.put_mapping(
        index='core',
        type='contact',
        body=json.dumps(CONTACT_MAPPING),
        callback=(yield gen.Callback('contact_mapping'))
    )

    es_connection.put_mapping(
        index='core',
        type='content',
        body=json.dumps(CONTENT_MAPPING),
        callback=(yield gen.Callback('content_mapping'))
    )

    es_connection.put_mapping(
        index='core',
        type='data',
        body=json.dumps(DATA_MAPPING),
        callback=(yield gen.Callback('data_mapping'))
    )

    es_connection.put_mapping(
        index='core',
        type='event',
        body=json.dumps(EVENT_MAPPING),
        callback=(yield gen.Callback('event_mapping'))
    )

    es_connection.put_mapping(
        index='core',
        type='location',
        body=json.dumps(LOCATION_MAPPING),
        callback=(yield gen.Callback('location_mapping'))
    )

    es_connection.put_mapping(
        index='core',
        type='search',
        body=json.dumps(SEARCH_MAPPING),
        callback=(yield gen.Callback('search_mapping'))
    )

    yield gen.Wait('event_mapping')
    yield gen.Wait('contact_mapping')
    yield gen.Wait('content_mapping')
    yield gen.Wait('data_mapping')
    yield gen.Wait('location_mapping')
    yield gen.Wait('search_mapping')

if __name__ == '__main__':
    port = 8001

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    # Django session information is used to authenticate the user making requests to the Tornado server
    # django.setup needs to be run to initialize the models used for sessions.
    django.setup()

    put_mappings()

    application = tornado.web.Application(patterns)

    print('Starting HTTP proxy...')  # noqa

    application.listen(port, address='127.0.0.1')

    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()

    print('Application listening on port %d...' % port)  # noqa
