import copy
import datetime
import json
import hashlib

from elasticsearch import Elasticsearch

from server import SOURCE_PATH, get_path
from server.contrib.pytoolbox import sort_dictionary
from server import settings


es = Elasticsearch(host=settings.ELASTICSEARCH['HOST'], port=settings.ELASTICSEARCH['PORT'], use_ssl=settings.ELASTICSEARCH['USE_SSL'])

initial_searches_path = get_path(SOURCE_PATH, 'contrib', 'estoolbox', 'initial_searches.json')
initial_searches = json.loads(open(initial_searches_path).read())


def create_initial_searches(user_id):
    for search in initial_searches:
        body = copy.deepcopy(search)

        query_and_filters = {}

        query_and_filters = {
            'filters': body['filters']
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
