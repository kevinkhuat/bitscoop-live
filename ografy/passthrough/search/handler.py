import json

import tornado.web
from tornado import gen
from tornadoes import ESConnection

from ografy import settings
from ografy.contrib.estoolbox.transform import (
    transform_structured_search, transform_text_search, transform_validate_dsl
)
from ografy.passthrough.auth import user_authenticated


# Implement SSL/CA CERTS
es_connection = ESConnection(
    settings.ELASTICSEARCH['HOST'],
    settings.ELASTICSEARCH['PORT']
)

content_type = 'application/json'


def _search_callback(self, response):
    self.write(json.loads(response.body))
    self.finish()


def _search(self, dsl_query):
    # TODO: Make this flexible
    index = "core"
    object_type = "event"

    es_connection.search(
        callback=_search_callback,
        index=index,
        type=object_type,
        source=dsl_query
    )


class StructuredSearch(tornado.web.RequestHandler):

    @user_authenticated
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug=None):
        if slug is not None:
            query = json.loads(self.get_argument('q'))
        else:
            query = json.load(slug)

        dsl_query = transform_structured_search(
            query=query,
            user_id=self.user.id
        )
        _search(self, dsl_query)

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class TextSearch(tornado.web.RequestHandler):

    @user_authenticated
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug=None):
        if slug is not None:
            query = json.loads(self.get_argument('q'))
        else:
            query = json.load(slug)

        dsl_query = transform_text_search(
            query=query,
            user_id=self.user.id
        )
        _search(self, dsl_query)

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class DSLSearch(tornado.web.RequestHandler):

    @user_authenticated
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, slug=None):
        if slug is not None:
            query = json.loads(self.get_argument('q'))
        else:
            query = json.load(slug)

        dsl_query = transform_validate_dsl(
            query=query,
            user_id=self.user.id
        )
        _search(self, dsl_query)

    @tornado.web.asynchronous
    def options(self):
        self.finish()
