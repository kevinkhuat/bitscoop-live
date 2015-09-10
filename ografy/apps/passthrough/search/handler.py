import json

import tornado.web
from tornado import gen
from tornadoes import ESConnection

from ografy import settings
from ografy.apps.passthrough.auth import user_authenticated
from ografy.apps.passthrough.documents import Search
from ografy.contrib.estoolbox.security import InvalidDSLQueryException, add_user_filter, validate_dsl
from ografy.contrib.pytoolbox import strip_invalid_key_characters


es_connection = ESConnection(
    settings.ELASTICSEARCH['HOST'],
    settings.ELASTICSEARCH['PORT']
)

content_type = 'application/json'


class ESSearch(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self, slug=None):

        @gen.coroutine
        def _search_callback(response):
            self.write(response.body.decode('utf-8'))
            new_search = Search(search_DSL=strip_invalid_key_characters(dsl_query), user_id=self.request.user.id)
            yield new_search.save()
            self.finish()

        def _search(dsl_query):
            # TODO: Make this flexible
            index = 'core'
            object_type = 'event'

            es_connection.search(
                callback=_search_callback,
                index=index,
                type=object_type,
                source=dsl_query
            )

        query = json.loads(self.get_argument('dsl'))

        try:
            validate_dsl(query)

            dsl_query = add_user_filter(query, self.request.user.id)

            _search(dsl_query)
        except InvalidDSLQueryException:
            self.send_error(400, mesg='Invalid DSL query. Please check the documentation')

    @tornado.web.asynchronous
    def options(self):
        self.finish()
