import copy
import datetime
import hashlib
import json

from elasticsearch import Elasticsearch

from server import SOURCE_PATH, get_path, settings
from server.contrib.pytoolbox import sort_dictionary


es = Elasticsearch(host=settings.ELASTICSEARCH['HOST'], port=settings.ELASTICSEARCH['PORT'], use_ssl=settings.ELASTICSEARCH['USE_SSL'])

initial_searches_path = get_path(SOURCE_PATH, 'contrib', 'estoolbox', 'initial_searches.json')
initial_searches = json.loads(open(initial_searches_path).read())


def create_initial_searches(user_id):
    for search in initial_searches:
        body = copy.deepcopy(search)

        filters = body['filters']

        unnamed_filters = copy.deepcopy(filters)

        for filter in unnamed_filters:
            del filter['name']

        query_and_filters = {
            'filters': unnamed_filters
        }

        if 'query' in body.keys() and body['query'] is not None:
            query_and_filters['query'] = body['query']

        sorted_dict = sort_dictionary(query_and_filters)
        hash_id = hashlib.sha512(sorted_dict.encode('utf-8')).hexdigest()

        body['user_id'] = user_id
        body['count'] = 1
        body['hash'] = hash_id
        body['last_run'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        es.index(index='core', doc_type='search', body=body)
