import json
from urllib.parse import urlencode

from tornado import gen
from tornado.concurrent import return_future
from tornado.escape import json_encode
from tornado.httpclient import HTTPRequest
from tornadoes import ESConnection


# This class extends the tornado-es library and includes useful methods that tornado-es does not have.
class ESBulkConnection(ESConnection):
    # This submits a bulk operation request.
    # It's called bulk_operation since the ElasticSearch bulk API allows you to do any combination
    # of operations (index, delete, put, etc.) in the same call.
    # For more info, see https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
    @return_future
    def bulk_operation(self, index, type, method='POST', body=None, parameters=None, callback=None):
        path = '/{index}/{type}/_bulk'.format(**locals())
        url = '%(url)s%(path)s?%(querystring)s' % {
            'url': self.url,
            'path': path,
            'querystring': urlencode(parameters or {})
        }
        request_arguments = dict(self.httprequest_kwargs)
        request_arguments['method'] = method

        # The bulk operations are located in the body
        if body is not None:
            request_arguments['body'] = body

        request = HTTPRequest(url, **request_arguments)
        self.client.fetch(request, callback)

    # The tornado-es search function had a bug where the call body was both being sent as the body and as a query parameter.
    # This was causing problems for ElasticSearch, so I rewrote it to avoid this problem.
    # The solution was pretty much just pulling the source body out first and deleting it from the arguments so it
    # won't be added as a query parameter.
    @return_future
    def search(self, callback, **kwargs):
        source = json_encode(kwargs.get('source', {
            'query': {
                'match_all': {}
            }
        }))
        del kwargs['source']
        path = self.create_path('search', **kwargs)

        self.post_by_path(path, callback, source)

    # This takes in a list of documents to be posted as well as a list of the unique IDs of those documents.
    # It searches for documents containing the IDs, and for every hit that it gets, it uses that ID on the index call
    # so that the operation acts as a PUT on the existing document rather than creating a new document.
    # ElasticSearch does not have uniqueness checks on anything other than _id, so unlike Mongo we cannot try
    # to insert a document and get an error on a uniqueness collision on some other field.
    @gen.coroutine
    def bulk_unique_post(self, index, type, document_list, id_list, body=None, parameters=None, callback=None):
        # search_end is used in pagination
        search_end = False
        # ElasticSearch's pagination returns size_parameter matches, starting at the document in from_parameter.
        # from parameter should be increased by size_parameter to get the next page.
        from_parameter = 0
        size_parameter = 1000
        # Stores documents that we're trying to index that have already been indexed
        present_documents = []

        # The ElasticSearch body for getting all documents whose unique IDs are in the unique ID list
        search_body = {
            'from': from_parameter,
            'size': size_parameter,
            'filter': {
                'terms': {
                    'identifier': id_list
                }
            }
        }

        # Keep paginating until told not to
        while not search_end:
            # Update the from parameter to get the next page
            search_body['from'] = from_parameter

            # Perform the search and save the response
            present_document_search = yield self.search(
                type=type,
                index=index,
                source=search_body
            )

            # Get the actual document hits from the search response
            decoded_result = json.loads(present_document_search.body.decode('utf-8'))['hits']['hits']
            # Add the documents from the search to the list of total results
            present_documents += decoded_result

            # If the number of results from this call is less than the size, then there are no more results
            # and we should end the search loop.
            if len(decoded_result) < size_parameter:
                search_end = True
            # If not, then there are probably more results, so get the next page.
            else:
                from_parameter += size_parameter

        existing_documents_dict = {}
        # Map the ES IDs to the unique IDs.
        for document in present_documents:
            existing_identifier = document['_source']['identifier']
            existing_id = document['_id']

            existing_documents_dict[existing_identifier] = existing_id

        existing_documents_keys = existing_documents_dict.keys()

        bulk_insert_body = ''

        # Construct the bulk insert body.
        for document in document_list:
            action_and_metadata = {
                'index': {
                    '_index': index,
                    '_type': type
                }
            }

            # If the document already exists, then add '_id' as a field in action_and_metadata['index'] so that
            # the operation updates the existing document instead of creating a new one.
            # If ElasticSearch is given an ID, it will automatically try to update an existing document with that
            # ID, and will only create a new document if none exists.
            if document['identifier'] in existing_documents_keys:
                action_and_metadata['index']['_id'] = existing_documents_dict[document['identifier']]

            bulk_insert_body += json.dumps(action_and_metadata) + '\n' + json.dumps(document) + '\n'

        # Call bulk_operation with the body that was just constructed.
        result = yield self.bulk_operation(
            type=type,
            index=index,
            body=bulk_insert_body
        )

        return result

    # This takes a list of terms, searches for documents of a given type that match those terms, then deletes them by their IDs.
    # ElasticSearch used to have a delete-on-search operation, where you could just tell it 'delete documents that
    # match this search', but they removed it since it caused some serious problems.  Without that, you have to delete
    # on ID, hence needing to do the search first.
    @gen.coroutine
    def bulk_delete(self, index, type, terms, body=None, parameters=None, callback=None):
        # search_end is used in pagination
        search_end = False
        # ElasticSearch's pagination returns size_parameter matches, starting at the document in from_parameter.
        # from parameter should be increased by size_parameter to get the next page.
        from_parameter = 0
        size_parameter = 1000
        # Stores documents that we're trying to index that have already been indexed
        matching_documents = []
        bulk_delete_body = ''

        # Construct the skeleton of the search body.  Search parameters will be added to the 'and' list just after this.
        search_body = {
            'from': from_parameter,
            'size': size_parameter,
            'filter': {
                'and': [
                ]
            }
        }

        # For each term, construct the ElasticSearch DSL syntax and add it to search_body['filter']['and']
        for key in terms:
            new_term = {
                'term': {
                    key: terms[key]
                }
            }
            search_body['filter']['and'].append(new_term)

        # Keep paginating until told not to
        while not search_end:
            # Update the from parameter to get the next page
            search_body['from'] = from_parameter

            # Perform the search and save the response
            present_document_search = yield self.search(
                type=type,
                index=index,
                source=search_body
            )

            # Get the actual document hits from the search response
            decoded_result = json.loads(present_document_search.body.decode('utf-8'))['hits']['hits']
            # Add the documents from the search to the list of total results
            matching_documents += decoded_result

            # If the number of results from this call is less than the size, then there are no more results
            # and we should end the search loop.
            if len(decoded_result) < size_parameter:
                search_end = True
            # If not, then there are probably more results, so get the next page.
            else:
                from_parameter += size_parameter

        # Construct the bulk deletion body.
        # Unlike a post, put, or get, deletion does not take a source after the action_and_metadata.
        for document in matching_documents:
            action_and_metadata = {
                'delete': {
                    '_index': index,
                    '_type': type,
                    '_id': document['_id']
                }
            }

            bulk_delete_body += json.dumps(action_and_metadata) + '\n'

        # Call bulk_operation with the body that was just constructed.
        result = yield self.bulk_operation(
            type=type,
            index=index,
            body=bulk_delete_body
        )

        return result

    @return_future
    def put_mapping(self, index, type, method='PUT', body=None, parameters=None, callback=None):
        path = '/{index}/_mapping/{type}'.format(**locals())
        url = '%(url)s%(path)s?%(querystring)s' % {
            'url': self.url,
            'path': path,
            'querystring': urlencode(parameters or {})
        }
        request_arguments = dict(self.httprequest_kwargs)
        request_arguments['method'] = method

        # The bulk operations are located in the body
        if body is not None:
            request_arguments['body'] = body

        request = HTTPRequest(url, **request_arguments)
        self.client.fetch(request, callback)
