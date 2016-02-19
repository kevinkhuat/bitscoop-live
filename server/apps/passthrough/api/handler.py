import datetime
import hashlib
import json
import urllib
from collections import OrderedDict

import jsonschema
import tornado.web
from django.conf import settings
from tornado import gen

from server.apps.passthrough.auth import user_authenticated
from server.apps.passthrough.documents import Connection, Settings
from server.contrib.estoolbox.security import InvalidDSLQueryException, InvalidTagExcpetion, validate_dsl, validate_tags
from server.contrib.estoolbox.security.validators import (
    CONTENT_TAG_VALIDATOR, EVENT_TAG_VALIDATOR, ORGANIZATION_TAG_VALIDATOR, PLACE_TAG_VALIDATOR, SEARCH_TEXT_FIELDS,
    THING_TAG_VALIDATOR
)
from server.contrib.estoolbox.tornadoes_bulk import ESBulkConnection
from server.contrib.locationtoolbox import estimation


es_connection = ESBulkConnection(
    settings.ELASTICSEARCH['HOST'],
    settings.ELASTICSEARCH['PORT']
)

es_connection.client.max_clients = 1000
es_connection.client.defaults['request_timeout'] = 1000
es_connection.client.defaults['connect_timeout'] = 1000

schema_json = json.loads(open('server/apps/passthrough/schema.json').read())


@gen.coroutine
def bulk_unique_post_and_id_replace(index, type, bulk_document_list, document_unique_id_list, document_id_mapping_dict):
    document_post_response = yield es_connection.bulk_unique_post(index, type, bulk_document_list, document_unique_id_list)
    document_post_response_decoded = json.loads(document_post_response.body.decode('utf-8'))['items']

    for index, document in enumerate(bulk_document_list):
        document_response_item = document_post_response_decoded[index]

        if 'create' in document_response_item.keys():
            document_id_mapping_dict[document['identifier']] = document_response_item['create']['_id']
        else:
            document_id_mapping_dict[document['identifier']] = document_response_item['index']['_id']


class EventHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self, slug=None):
        limit = self.get_arguments('limit')

        if len(limit) > 0:
            limit = json.loads(limit[0])

        offset = self.get_arguments('offset')

        if len(offset) > 0:
            offset = json.loads(offset[0])
        else:
            offset = 0

        filters = self.get_arguments('filters')

        if len(filters) > 0:
            filters = json.loads(filters[0])
            try:
                validate_dsl(filters)
            except InvalidDSLQueryException:
                self.send_error(400, mesg='Invalid DSL query. Please check the documentation')
        else:
            filters = {
                'bool': {
                    'must': [],
                    'must_not': [],
                    'should': []
                }
            }

        query = {
            'query': {
                'bool': {
                    'filter': {
                        'and': [
                            filters,
                            {
                                'bool': {
                                    'must': [
                                        {
                                            'term': {
                                                'user_id': self.request.user.id
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            },
            'size': limit,
            'from': offset
        }

        sort_field = self.get_arguments('sort_field')

        if len(sort_field) > 0:
            sort_field = sort_field[0]

            sort_order = self.get_arguments('sort_order')

            if len(sort_order) > 0:
                sort_order = sort_order[0]
            else:
                sort_order = 'desc'
        else:
            sort_field = '_score'
            sort_order = 'desc'

        q = self.get_arguments('q')

        if len(q) > 0 and q[0] != '' and q[0] != '[]':
            query['query']['bool']['must'] = {
                'multi_match': {
                    'query': q,
                    'type': 'most_fields',
                    'fields': SEARCH_TEXT_FIELDS
                }
            }
        else:
            q = ''
            sort_field = 'datetime'

        query['sort'] = [
            {
                sort_field: {
                    'order': sort_order
                }
            }
        ]

        index = 'core'
        object_type = 'event'

        response = yield es_connection.search(
            index=index,
            type=object_type,
            source=query
        )

        cleaned_results = []
        body_decoded = json.loads(response.body.decode('utf-8'))
        result_total = body_decoded['hits']['total']
        results = body_decoded['hits']['hits']

        for result in results:
            cleaned_result = result['_source']
            cleaned_result['id'] = result['_id']
            if hasattr(result, '_score'):
                cleaned_result['relevance'] = result['_score']
            else:
                cleaned_result['relevance'] = ''

            cleaned_results.append(cleaned_result)

        search_response = {
            'results': cleaned_results,
            'count': result_total
        }

        if offset == 0:
            search_response['prev'] = None
        else:
            url_parts = list(urllib.parse.urlparse(self.request.uri))
            url_parts[0] = 'https'
            url_parts[1] = self.request.host
            url_parts[4] = urllib.parse.urlencode({
                'limit': limit,
                'offset': offset - limit,
                'q': q,
                'filters': json.dumps(filters),
                'sort_field': sort_field,
                'sort_order': sort_order
            })

            previous_url = urllib.parse.urlunparse(url_parts)

            search_response['prev'] = previous_url

        if limit + offset >= result_total:
            search_response['next'] = None
        else:
            url_parts = list(urllib.parse.urlparse(self.request.uri))
            url_parts[0] = 'https'
            url_parts[1] = self.request.host
            url_parts[4] = urllib.parse.urlencode({
                'limit': limit,
                'offset': offset + limit,
                'q': q,
                'filters': json.dumps(filters),
                'sort_field': sort_field,
                'sort_order': sort_order
            })

            next_url = urllib.parse.urlunparse(url_parts)

            search_response['next'] = next_url

        self.write(search_response)
        self.finish()

    # Posting Events is a multi-step process that actually involves posting associated Contacts, Content, and Data, and
    # posting every one of these document types requires a uniqueness check so that the same document isn't posted
    # more than once.
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def post(self, slug=None):
        # Each document type needs a few different lists/dictionaries for the insertion process.
        # The bulk list is just a list of all of the documents that are going to be inserted.
        bulk_contact_list = []
        # The unique ID list is a list of all the unique IDs of documents that are going to be inserted.
        # It is used to make sure that the same document isn't added more than once.  For example, if a number of
        # Twitter direct messages are from the same person, we only want to attempt to insert that Contact once.
        contact_unique_id_list = []
        # The mapping dictionary is used to store the ElasticSearch IDs of documents that are already present
        # in the database.  The keys are unique IDs and the values are ElasticSearch IDs.
        contact_id_mapping_dict = {}

        bulk_content_list = []
        content_unique_id_list = []
        content_id_mapping_dict = {}

        bulk_organization_list = []
        organization_unique_id_list = []
        organization_id_mapping_dict = {}

        bulk_place_list = []
        place_unique_id_list = []
        place_id_mapping_dict = {}

        bulk_thing_list = []
        thing_unique_id_list = []
        thing_id_mapping_dict = {}

        bulk_event_list = []
        event_unique_id_list = []

        # Get and decode the list of Events.
        post_event_list = json.loads(self.get_argument('events'))
        # Get the user's ID
        user_id = self.request.user.id

        # Iterate through each new Event
        for post_event in post_event_list:
            # These are lists of the data IDs, contacts, and content documents that are associated with this Event,
            # as opposed to the bulk_<document>_lists which contain all of that type across all of the
            # events being posted
            event_organizations = []
            event_contacts = []
            event_content = []
            event_places = []
            event_things = []

            # Parse each Contact object associated with this Event
            for contact in post_event['contacts']:
                # Add the Connection ID.
                contact['connection'] = post_event['connection']
                # Add the user ID.
                contact['user_id'] = user_id

                # Only add the current Contact object's unique ID to the unique ID list if it isn't already present.
                # This is to prevent the same document from being indexed multiple times.
                if contact['identifier'] not in contact_unique_id_list:
                    # Add a copy of the Contact object to the global list of all Contacts being inserted
                    bulk_contact_list.append(contact.copy())
                    # Add the Contact's unique ID to the list of unique IDs of Contacts being inserted
                    contact_unique_id_list.append(contact['identifier'])

                # The local copy of the Contact present in the Event does not need the user ID, Connection ID or data ID list
                # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                del contact['user_id']
                del contact['connection']
                # The local copy of the Contact also does not need the unique ID.  It will need the ElasticSearch ID
                # of the entry in the Contact collection, but we don't have that yet since it hasn't been indexed.
                # In the interim, have the ES ID field store the unique ID; once Contacts have been indexed,
                # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                contact['contact'] = contact['identifier']
                # Delete the unique ID field
                del contact['identifier']

                # Add the local copy of the Contact to the list of Contacts this Event references.
                event_contacts.append(contact)

            # Parse each Organization object associated with this Event
            for organization in post_event['organizations']:
                # If an invalid Organization is posted, it will not be indexed in ES nor will it be added to the parent Event
                valid_organization = True

                try:
                    validate_tags(organization, ORGANIZATION_TAG_VALIDATOR)
                except InvalidTagExcpetion:
                    valid_organization = False

                if valid_organization:
                    # Add the Connection ID.
                    organization['connection'] = post_event['connection']
                    # Add the user ID.
                    organization['user_id'] = user_id

                    # Only add the current Organization object's unique ID to the unique ID list if it isn't already present.
                    # This is to prevent the same document from being indexed multiple times.
                    if organization['identifier'] not in organization_unique_id_list:
                        # Add a copy of the Organization object to the global list of all Organizations being inserted
                        bulk_organization_list.append(organization.copy())
                        # Add the Organization's unique ID to the list of unique IDs of Organizations being inserted
                        organization_unique_id_list.append(organization['identifier'])

                    # The local copy of the Organization present in the Event does not need the user ID, Connection ID or data ID list
                    # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                    del organization['user_id']
                    del organization['connection']
                    # The local copy of the Organization also does not need the unique ID.  It will need the ElasticSearch ID
                    # of the entry in the Organization collection, but we don't have that yet since it hasn't been indexed.
                    # In the interim, have the ES ID field store the unique ID; once Organizations have been indexed,
                    # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                    organization['organization'] = organization['identifier']
                    # Delete the unique ID field
                    del organization['identifier']

                    # Add the local copy of the Organization to the list of Organizations this Event references.
                    event_organizations.append(organization)

            # Parse each Content object associated with this Event
            for content in post_event['content']:
                # If an invalid Content is posted, it will not be indexed in ES nor will it be added to the parent Event
                valid_content = True

                try:
                    validate_tags(content, CONTENT_TAG_VALIDATOR)
                except InvalidTagExcpetion:
                    valid_content = False

                if valid_content:
                    # Add the Connection ID.
                    content['connection'] = post_event['connection']
                    # Add the user ID.
                    content['user_id'] = user_id

                    # Only add the current Content object's unique ID to the unique ID list if it isn't already present.
                    # This is to prevent the same document from being indexed multiple times.
                    if content['identifier'] not in content_unique_id_list:
                        # Add a copy of the Content object to the global list of all Content being inserted
                        bulk_content_list.append(content.copy())
                        # Add the Content's unique ID to the list of unique IDs of Content being inserted
                        content_unique_id_list.append(content['identifier'])

                    # The local copy of the Content present in the Event does not need the user ID, Connection ID or data ID list
                    # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                    del content['user_id']
                    del content['connection']
                    # The local copy of the Content also does not need the unique ID.  It will need the ElasticSearch ID
                    # of the entry in the Content collection, but we don't have that yet since it hasn't been indexed.
                    # In the interim, have the ES ID field store the unique ID; once Contents have been indexed,
                    # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                    content['content'] = content['identifier']
                    # Delete the unique ID field
                    del content['identifier']

                    # Add the local copy of the Content to the list of Content this Event references.
                    event_content.append(content)

            for place in post_event['places']:
                # If an invalid Place is posted, it will not be indexed in ES nor will it be added to the parent Event
                valid_place = True

                try:
                    validate_tags(place, PLACE_TAG_VALIDATOR)
                except InvalidTagExcpetion:
                    valid_place = False

                if valid_place:
                    # Add the Connection ID.
                    place['connection'] = post_event['connection']
                    # Add the user ID.
                    place['user_id'] = user_id

                    # Only add the current Content object's unique ID to the unique ID list if it isn't already present.
                    # This is to prevent the same document from being indexed multiple times.
                    if place['identifier'] not in place_unique_id_list:
                        # Add a copy of the Content object to the global list of all Content being inserted
                        bulk_place_list.append(place.copy())
                        # Add the Content's unique ID to the list of unique IDs of Content being inserted
                        place_unique_id_list.append(place['identifier'])

                    # The local copy of the Content present in the Event does not need the user ID, Connection ID or data ID list
                    # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                    del place['user_id']
                    del place['connection']
                    # The local copy of the Content also does not need the unique ID.  It will need the ElasticSearch ID
                    # of the entry in the Content collection, but we don't have that yet since it hasn't been indexed.
                    # In the interim, have the ES ID field store the unique ID; once Contents have been indexed,
                    # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                    place['place'] = place['identifier']
                    # Delete the unique ID field
                    del place['identifier']

                    # Add the local copy of the Content to the list of Content this Event references.
                    event_places.append(place)

            # Parse each Thing object associated with this Event
            for thing in post_event['things']:
                # If an invalid Thing is posted, it will not be indexed in ES nor will it be added to the parent Event
                valid_thing = True

                try:
                    validate_tags(thing, THING_TAG_VALIDATOR)
                except InvalidTagExcpetion:
                    valid_thing = False

                if valid_thing:
                    # Add the Connection ID.
                    thing['connection'] = post_event['connection']
                    # Add the user ID.
                    thing['user_id'] = user_id

                    # Only add the current Thing object's unique ID to the unique ID list if it isn't already present.
                    # This is to prevent the same document from being indexed multiple times.
                    if thing['identifier'] not in thing_unique_id_list:
                        # Add a copy of the Thing object to the global list of all Thing being inserted
                        bulk_thing_list.append(thing.copy())
                        # Add the Thing's unique ID to the list of unique IDs of Thing being inserted
                        thing_unique_id_list.append(thing['identifier'])

                    # The local copy of the Thing present in the Event does not need the user ID, Connection ID or data ID list
                    # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                    del thing['user_id']
                    del thing['connection']
                    # The local copy of the Thing also does not need the unique ID.  It will need the ElasticSearch ID
                    # of the entry in the Thing collection, but we don't have that yet since it hasn't been indexed.
                    # In the interim, have the ES ID field store the unique ID; once Things have been indexed,
                    # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                    thing['thing'] = thing['identifier']
                    # Delete the unique ID field
                    del thing['identifier']

                    # Add the local copy of the Thing to the list of Thing this Event references.
                    event_things.append(thing)

            # If the Event did not have something that could be mapped to a Location, that field will be blank.
            # In this case, the Location will need to be estimated.
            if 'location' not in post_event.keys():
                # If the Event did not have a datetime, then use the current datetime.
                if 'datetime' not in post_event.keys():
                    post_event['datetime'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

                # Estimate the Location.
                post_event['location'] = yield estimation.estimate(post_event['user_id'], post_event['datetime'])
            # If the Event did have Location information, then use that and insert it into the database.
            else:
                action_and_metadata = {
                    'index': {
                        '_index': 'core',
                        '_type': 'location'
                    }
                }

                document = post_event['location']
                document['user_id'] = user_id

                bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(document) + '\n'

                yield es_connection.bulk_operation(
                    type='location',
                    index='core',
                    body=bulk_insert_body
                )

            # If an invalid Event is posted, it will not be indexed in ES nor will it be added to the parent Event
            valid_event = True

            try:
                validate_tags(post_event, EVENT_TAG_VALIDATOR)
            except InvalidTagExcpetion:
                valid_event = False

            if valid_event:
                # Make copies of the lists of documents/IDs that the Event references.
                post_event['organizations'] = event_organizations.copy()
                post_event['contacts'] = event_contacts.copy()
                post_event['content'] = event_content.copy()
                post_event['places'] = event_places.copy()
                # Add the user ID.
                post_event['user_id'] = user_id

                # Add the Event object to the global list of all Events being inserted
                bulk_event_list.append(post_event.copy())
                # Add the Event's unique ID to the list of unique IDs of Events being inserted
                event_unique_id_list.append(post_event['identifier'])

        # If there are Organizations, Contacts, Content, Places, or Things to be indexed, then do so.
        # bulk_unique_post_and_id_replace will populate the unique ID list with the necessary key-value relations
        # between unique IDs and ElasticSearch IDs.
        # The callback using gen.Callback allows for us to wait until any point in the code for that to finish before
        # continuing, and allows for multiple asynchronous functions to be run simultaneously while still waiting for
        # all to finish before proceeding.
        if len(bulk_organization_list) > 0:
            bulk_unique_post_and_id_replace('core', 'organization', bulk_organization_list, organization_unique_id_list, organization_id_mapping_dict, callback=(yield gen.Callback('organization_bulk_unique_post_and_id_replace')))
        if len(bulk_contact_list) > 0:
            bulk_unique_post_and_id_replace('core', 'contact', bulk_contact_list, contact_unique_id_list, contact_id_mapping_dict, callback=(yield gen.Callback('contact_bulk_unique_post_and_id_replace')))
        if len(bulk_content_list) > 0:
            bulk_unique_post_and_id_replace('core', 'content', bulk_content_list, content_unique_id_list, content_id_mapping_dict, callback=(yield gen.Callback('content_bulk_unique_post_and_id_replace')))
        if len(bulk_place_list) > 0:
            bulk_unique_post_and_id_replace('core', 'place', bulk_place_list, place_unique_id_list, place_id_mapping_dict, callback=(yield gen.Callback('place_bulk_unique_post_and_id_replace')))
        if len(bulk_thing_list) > 0:
            bulk_unique_post_and_id_replace('core', 'thing', bulk_thing_list, thing_unique_id_list, thing_id_mapping_dict, callback=(yield gen.Callback('thing_bulk_unique_post_and_id_replace')))

        # These wait for the Contact bulk unique post and the Content bulk post to finish, but in each case only if there
        # were any of that document type to post.
        # This is structured so that both operations can run at the same time, rather than doing the Contact bulk post
        # and waiting for it to finish before doing the Content bulk post.  The Event bulk posting will not occur until
        # both of those operations are complete (or just one if only one needs to be run; if neither need to be run,
        # then this would be skipped entirely).
        if len(bulk_organization_list) > 0:
            yield gen.Wait('organization_bulk_unique_post_and_id_replace')
        if len(bulk_contact_list) > 0:
            yield gen.Wait('contact_bulk_unique_post_and_id_replace')
        if len(bulk_content_list) > 0:
            yield gen.Wait('content_bulk_unique_post_and_id_replace')
        if len(bulk_place_list) > 0:
            yield gen.Wait('place_bulk_unique_post_and_id_replace')
        if len(bulk_thing_list) > 0:
            yield gen.Wait('thing_bulk_unique_post_and_id_replace')

        # Now that the Copmanies, Contacts, Content, Places, and Things are indexed, as well as the Data that had been completed prior to those two,
        # the ID mapping dictionary has key-value relations between the unique IDs of each associated document
        # and the ElasticSearch IDs of the Data, Organization, Contact, and Content documents corresponding to those unique IDs.
        # Use these mapping dictionaries to replace all of the unique IDs in every Event with the associated ES ID.
        for event in bulk_event_list:
            for organization in event['organizations']:
                organization['organization'] = organization_id_mapping_dict[organization['organization']]

            for contact in event['contacts']:
                contact['contact'] = contact_id_mapping_dict[contact['contact']]

            for content in event['content']:
                content['content'] = content_id_mapping_dict[content['content']]

            for place in event['places']:
                place['place'] = place_id_mapping_dict[place['place']]

            for thing in event['things']:
                thing['thing'] = thing_id_mapping_dict[thing['thing']]

        # Post the Events.  There's no need to use the ID replacement version of bulk_unique_post since nothing
        # references the Events and thus there's no need to save the unique ID as a placeholder for an ES ID.
        event_post_response = yield es_connection.bulk_unique_post('core', 'event', bulk_event_list, event_unique_id_list)
        # Decode the response so that it can be sent back to the client that made the call.
        event_post_response_decoded = json.loads(event_post_response.body.decode('utf-8'))

        self.write(event_post_response_decoded)
        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def put(self):
        user = self.request.user
        user_id = user.id

        body = json.loads(self.request.body.decode('utf-8'))
        filter_types = body['filters']

        if 'query' in body.keys():
            search_query = body['query']
        else:
            search_query = None

        if 'namedFilters' in body.keys():
            named_filters = body['namedFilters']
        else:
            named_filters = None

        structure_schema = schema_json['structure']
        who_schema = schema_json['who']
        what_schema = schema_json['what']
        when_schema = schema_json['when']
        where_schema = schema_json['where']
        connector_schema = schema_json['connector']

        jsonschema.validate(filter_types, structure_schema)

        json_valid = True

        for type in filter_types:
            for filter in filter_types[type]:
                matched_schema = False

                for schema in [who_schema, what_schema, when_schema, where_schema, connector_schema]:
                    try:
                        validate_filter(filter, schema)
                        matched_schema = True
                    except jsonschema.ValidationError:
                        pass
                    except jsonschema.SchemaError as err:
                        self.send_error(400, err)

                if not matched_schema:
                    json_valid = False

        if json_valid:
            if search_query is not None:
                query_and_filters = {
                    'query': search_query,
                    'filters': filter_types
                }
            else:
                query_and_filters = filter_types

            sorted_dict = sort_dictionary(query_and_filters)
            hash_id = hashlib.sha512(sorted_dict.encode('utf-8')).hexdigest()

            query = {
                'query': {
                    'bool': {
                        'filter': {
                            'bool': {
                                'must': [
                                    {
                                        'term': {
                                            'hash': hash_id
                                        }
                                    },
                                    {
                                        'term': {
                                            'user_id': user_id
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

            index = 'core'
            object_type = 'search'

            search_response = yield es_connection.search(
                index=index,
                type=object_type,
                source=query
            )

            body_decoded = json.loads(search_response.body.decode('utf-8'))
            result_total = body_decoded['hits']['total']
            results = body_decoded['hits']['hits']

            if result_total > 0:
                id = results[0]['_id']

                contents = {
                    'doc': {
                        'last_run': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                        'count': results[0]['_source']['count'] + 1,
                    }
                }

                if named_filters is not None:
                    contents['doc']['named_filters'] = named_filters

                action_and_metadata = {
                    'update': {
                        '_index': 'core',
                        '_type': 'search',
                        '_id': id
                    }
                }

                bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

                yield es_connection.bulk_operation(
                    type='search',
                    index='core',
                    body=bulk_insert_body
                )
            else:
                contents = {
                    'count': 1,
                    'filters': filter_types,
                    'hash': hash_id,
                    'last_run': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                    'user_id': user_id
                }

                if named_filters is not None:
                    contents['named_filters'] = named_filters

                if search_query is not None:
                    contents['query'] = search_query

                action_and_metadata = {
                    'index': {
                        '_index': 'core',
                        '_type': 'search'
                    }
                }

                bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

                index_response = yield es_connection.bulk_operation(
                    type='search',
                    index='core',
                    body=bulk_insert_body
                )

                body_decoded = json.loads(index_response.body.decode('utf-8'))
                id = body_decoded['items'][0]['create']['_id']

            self.write({'searchID': id})
            self.finish()
        else:
            self.send_error(400, mesg='Invalid filter JSON. Please check the documentation')

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class SearchesHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self):
        user = self.request.user
        user_id = user.id

        filters = self.get_arguments('filters')
        input_query = self.get_arguments('query')

        if len(filters) > 0:
            filters = json.loads(filters[0])
        else:
            filters = None

        if len(input_query) > 0:
            input_query = input_query[0]
        else:
            input_query = None

        if input_query is None and filters is None:
            search_tab = self.get_arguments('searchTab')[0]
            size = self.get_arguments('limit')[0]
            start_from = self.get_arguments('offset')[0]

            query = {
                'query': {
                    'bool': {
                        'filter': {
                            'bool': {
                                'must': [
                                    {
                                        'term': {
                                            'user_id': user_id
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
                'size': size,
                'from': start_from
            }

            if search_tab == 'favorited':
                query['query']['bool']['filter']['bool']['must'].append({
                    'term': {
                        'favorited': True
                    }
                })
                query['sort'] = [{
                    'name': 'asc',
                    'last_run': 'desc'
                }]
            elif search_tab == 'recent':
                query['sort'] = [{'last_run': 'desc'}]
            elif search_tab == 'top':
                query['sort'] = [{
                    'count': 'asc',
                    'last_run': 'desc'
                }]

            index = 'core'
            object_type = 'search'

            search_response = yield es_connection.search(
                index=index,
                type=object_type,
                source=query
            )

            body_decoded = json.loads(search_response.body.decode('utf-8'))
            results = body_decoded['hits']['hits']

            self.write({
                'results': results
            })
            self.finish()
        else:
            structure_schema = schema_json['structure']
            who_schema = schema_json['who']
            what_schema = schema_json['what']
            when_schema = schema_json['when']
            where_schema = schema_json['where']
            connector_schema = schema_json['connector']

            jsonschema.validate(filters, structure_schema)

            json_valid = True

            for type in filters:
                for filter in filters[type]:
                    matched_schema = False

                    for schema in [who_schema, what_schema, when_schema, where_schema, connector_schema]:
                        try:
                            validate_filter(filter, schema)
                            matched_schema = True
                        except jsonschema.ValidationError:
                            pass
                        except jsonschema.SchemaError as err:
                            self.send_error(400, err)

                    if not matched_schema:
                        json_valid = False

            if json_valid:
                if input_query is not None:
                    query_and_filters = {
                        'query': input_query,
                        'filters': filters
                    }
                else:
                    query_and_filters = filters

                sorted_dict = sort_dictionary(query_and_filters)
                hash_id = hashlib.sha512(sorted_dict.encode('utf-8')).hexdigest()

                query = {
                    'query': {
                        'bool': {
                            'filter': {
                                'bool': {
                                    'must': [
                                        {
                                            'term': {
                                                'hash': hash_id
                                            }
                                        },
                                        {
                                            'term': {
                                                'user_id': user_id
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }

                index = 'core'
                object_type = 'search'

                search_response = yield es_connection.search(
                    index=index,
                    type=object_type,
                    source=query
                )

                body_decoded = json.loads(search_response.body.decode('utf-8'))
                result_total = body_decoded['hits']['total']
                results = body_decoded['hits']['hits']

                if result_total > 0:
                    result = results[0]['_source']
                    result_keys = result.keys()
                    return_dict = {}

                    if 'name' in result_keys:
                        return_dict['name'] = result['name']

                    if 'icon' in result_keys:
                        return_dict['icon'] = result['icon']
                        return_dict['iconColor'] = result['icon_color']

                    if 'favorited' in result_keys:
                        return_dict['favorited'] = result['favorited']

                    if 'named_filters' in result_keys:
                        return_dict['named_filters'] = result['named_filters']

                    return_dict['searchID'] = results[0]['_id']

                    self.write(return_dict)
                    self.finish()
                else:
                    self.write({
                        'search_not_found': True
                    })
                    self.finish()
            else:
                self.send_error(400, mesg='Invalid filter JSON. Please check the documentation')

    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def put(self):
        user = self.request.user
        user_id = user.id

        body = json.loads(self.request.body.decode('utf-8'))

        if 'namedFilters' in body.keys():
            named_filters = body['namedFilters']
        else:
            named_filters = None

        filter_types = body['filters']

        if 'query' in body.keys():
            search_query = body['query']
        else:
            search_query = None

        structure_schema = schema_json['structure']
        who_schema = schema_json['who']
        what_schema = schema_json['what']
        when_schema = schema_json['when']
        where_schema = schema_json['where']
        connector_schema = schema_json['connector']

        jsonschema.validate(filter_types, structure_schema)

        json_valid = True

        for type in filter_types:
            for filter in filter_types[type]:
                matched_schema = False

                for schema in [who_schema, what_schema, when_schema, where_schema, connector_schema]:
                    try:
                        validate_filter(filter, schema)
                        matched_schema = True
                    except jsonschema.ValidationError:
                        pass
                    except jsonschema.SchemaError as err:
                        self.send_error(400, err)

                if not matched_schema:
                    json_valid = False

        if json_valid:
            if search_query is not None:
                query_and_filters = {
                    'query': search_query,
                    'filters': filter_types
                }
            else:
                query_and_filters = filter_types

            sorted_dict = sort_dictionary(query_and_filters)
            hash_id = hashlib.sha512(sorted_dict.encode('utf-8')).hexdigest()

            contents = {
                'count': 1,
                'favorited': True,
                'filters': filter_types,
                'hash': hash_id,
                'last_run': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'user_id': user_id
            }

            if 'name' in body.keys() and body['name'] != '':
                contents['name'] = body['name']

            if 'icon' in body.keys() and body['icon'] != '':
                contents['icon'] = body['icon']

                contents['icon_color'] = body['iconColor']

            if search_query is not None:
                contents['query'] = search_query

            if named_filters is not None:
                contents['named_filters'] = named_filters

            action_and_metadata = {
                'index': {
                    '_index': 'core',
                    '_type': 'search'
                }
            }

            bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

            index_response = yield es_connection.bulk_operation(
                type='search',
                index='core',
                body=bulk_insert_body
            )

            body_decoded = json.loads(index_response.body.decode('utf-8'))
            id = body_decoded['items'][0]['create']['_id']

            self.write({'searchID': id})
            self.finish()
        else:
            self.send_error(400, mesg='Invalid filter JSON. Please check the documentation')

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class SearchesIDHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self, search_id):
        user = self.request.user
        user_id = user.id

        query = {
            'query': {
                'bool': {
                    'filter': {
                        'bool': {
                            'must': [
                                {
                                    'term': {
                                        '_id': search_id
                                    }
                                },
                                {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        index = 'core'
        object_type = 'search'

        search_response = yield es_connection.search(
            index=index,
            type=object_type,
            source=query
        )

        body_decoded = json.loads(search_response.body.decode('utf-8'))
        result_total = body_decoded['hits']['total']
        results = body_decoded['hits']['hits']

        if result_total > 0:
            result = results[0]['_source']
            result_keys = result.keys()
            return_dict = {}

            if 'query' in result_keys:
                return_dict['query'] = result['query']

            if 'filters' in result_keys:
                return_dict['filters'] = result['filters']

            if 'name' in result_keys:
                return_dict['name'] = result['name']

            if 'icon' in result_keys:
                return_dict['icon'] = result['icon']
                return_dict['iconColor'] = result['icon_color']

            if 'favorited' in result_keys:
                return_dict['favorited'] = result['favorited']

            if 'named_filters' in result_keys:
                return_dict['named_filters'] = result['named_filters']

            self.write(return_dict)
            self.finish()
        else:
            self.write({
                'search_not_found': True
            })
            self.finish()

    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def put(self, search_id):
        user = self.request.user
        user_id = user.id

        body = json.loads(self.request.body.decode('utf-8'))

        if 'namedFilters' in body.keys():
            named_filters = body['namedFilters']
        else:
            named_filters = None

        query = {
            'query': {
                'bool': {
                    'filter': {
                        'bool': {
                            'must': [
                                {
                                    'term': {
                                        '_id': search_id
                                    }
                                },
                                {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        index = 'core'
        object_type = 'search'

        search_response = yield es_connection.search(
            index=index,
            type=object_type,
            source=query
        )

        body_decoded = json.loads(search_response.body.decode('utf-8'))
        result_total = body_decoded['hits']['total']

        if result_total > 0:
            put_body = {}

            if 'name' in body.keys():
                put_body['name'] = body['name']
            else:
                put_body['name'] = ''

            if 'icon' in body.keys():
                put_body['icon'] = body['icon']
                put_body['icon_color'] = body['iconColor']
            else:
                put_body['icon'] = ''
                put_body['icon_color'] = ''

            put_body['favorited'] = True

            if named_filters is not None:
                put_body['named_filters'] = named_filters

            contents = {
                'doc': put_body
            }

            action_and_metadata = {
                'update': {
                    '_index': 'core',
                    '_type': 'search',
                    '_id': search_id
                }
            }

            bulk_put_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

            yield es_connection.bulk_operation(
                type='search',
                index='core',
                body=bulk_put_body
            )

            self.write({'searchID': search_id})
            self.finish()
        else:
            filter_types = body['filters']

            if 'query' in body.keys():
                search_query = body['query']
            else:
                search_query = None

            structure_schema = schema_json['structure']
            who_schema = schema_json['who']
            what_schema = schema_json['what']
            when_schema = schema_json['when']
            where_schema = schema_json['where']
            connector_schema = schema_json['connector']

            jsonschema.validate(filter_types, structure_schema)

            json_valid = True

            for type in filter_types:
                for filter in filter_types[type]:
                    matched_schema = False

                    for schema in [who_schema, what_schema, when_schema, where_schema, connector_schema]:
                        try:
                            validate_filter(filter, schema)
                            matched_schema = True
                        except jsonschema.ValidationError:
                            pass
                        except jsonschema.SchemaError as err:
                            self.send_error(400, err)

                    if not matched_schema:
                        json_valid = False

            if json_valid:
                if search_query is not None:
                    query_and_filters = {
                        'query': search_query,
                        'filters': filter_types
                    }
                else:
                    query_and_filters = filter_types

                sorted_dict = sort_dictionary(query_and_filters)
                hash_id = hashlib.sha512(sorted_dict.encode('utf-8')).hexdigest()

                contents = {
                    'count': 1,
                    'favorited': True,
                    'filters': filter_types,
                    'hash': hash_id,
                    'last_run': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                    'user_id': user_id
                }

                if body['name'] != '':
                    contents['name'] = body['name']

                if body['icon'] != '':
                    contents['icon'] = body['icon']

                    contents['icon_color'] = body['iconColor']

                if search_query is not None:
                    contents['query'] = search_query

                if named_filters is not None:
                    contents['named_filters'] = named_filters

                action_and_metadata = {
                    'index': {
                        '_index': 'core',
                        '_type': 'search'
                    }
                }

                bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

                index_response = yield es_connection.bulk_operation(
                    type='search',
                    index='core',
                    body=bulk_insert_body
                )

                body_decoded = json.loads(index_response.body.decode('utf-8'))
                id = body_decoded['items'][0]['create']['_id']

                self.write({'searchID': id})
                self.finish()
            else:
                self.send_error(400, mesg='Invalid filter JSON. Please check the documentation')

    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self, search_id):
        user = self.request.user
        user_id = user.id

        query = {
            'query': {
                'bool': {
                    'filter': {
                        'bool': {
                            'must': [
                                {
                                    'term': {
                                        '_id': search_id
                                    }
                                },
                                {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        index = 'core'
        object_type = 'search'

        search_response = yield es_connection.search(
            index=index,
            type=object_type,
            source=query
        )

        body_decoded = json.loads(search_response.body.decode('utf-8'))
        result_total = body_decoded['hits']['total']

        if result_total > 0:
            action_and_metadata = {
                'update': {
                    '_index': 'core',
                    '_type': 'search',
                    '_id': search_id
                }
            }

            contents = {
                'doc': {
                    'name': '',
                    'icon': '',
                    'icon_color': '',
                    'favorited': False
                }
            }

            bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(contents) + '\n'

            index_response = yield es_connection.bulk_operation(
                type='search',
                index='core',
                body=bulk_insert_body
            )

            self.write({'searchID': search_id})
            self.finish()

    @tornado.web.asynchronous
    def options(self, search_id):
        self.finish()


class LocationHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def post(self, slug=None):
        post_location = json.loads(self.get_argument('location'))
        post_location['user_id'] = self.request.user.id

        action_and_metadata = {
            'index': {
                '_index': 'core',
                '_type': 'location'
            }
        }

        bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(post_location) + '\n'

        response = yield es_connection.bulk_operation(
            type='location',
            index='core',
            body=bulk_insert_body
        )

        self.write(json.loads(response.body.decode('utf-8')))
        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class EstimateLocationHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self, slug=None):
        settings = Settings.objects.get(user_id=self.request.user.id)
        next_estimate_date = settings.last_estimate_all_locations + datetime.timedelta(days=5)
        new_estimate_allowed = datetime.datetime.utcnow() > next_estimate_date

        if new_estimate_allowed:
            estimation.reestimate_all(self.request.user.id)

            self.set_status(200, 'Re-estimation successful.')
        else:
            self.set_status(400, 'Re-estimation not allowed yet.')

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class ConnectionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self, slug=None):
        user_id = self.request.user.id
        connection_id_to_delete = self.get_argument('connection_id')

        delete_connection_and_linked_documents(connection_id_to_delete, user_id)

        self.write('Deletion successful')
        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class AccountHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self):
        user = self.request.user
        user_id = user.id

        Settings.objects.filter(user_id=user_id).delete()
        Connection.objects.filter(user_id=user_id).find_all(callback=(yield gen.Callback('connection_get')))

        delete_user_documents('search', user_id)
        delete_user_documents('location', user_id)

        connections = yield gen.Wait('connection_get')

        for connection in connections:
            delete_connection_and_linked_documents(str(connection._id), user_id)

        user.delete()

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


@gen.coroutine
def delete_connection_and_linked_documents(connection_id, user_id):
    connection_to_delete = yield Connection.objects.get(id=connection_id, user_id=user_id)
    index = 'core'

    terms = {
        'user_id': user_id,
        'connection': connection_id
    }

    for type in ['organization', 'contact', 'content', 'event', 'place', 'thing']:
        es_connection.bulk_delete(index, type, terms)

    yield connection_to_delete.delete()


@gen.coroutine
def delete_user_documents(doc_type, user_id):
    index = 'core'

    terms = {
        'user_id': user_id
    }

    es_connection.bulk_delete(index, doc_type, terms)


def validate_filter(dict, schema):
    if 'And' in dict.keys():
        for single_filter in dict['And']:
            if single_filter is not None:
                validate_filter(single_filter, schema)
    elif 'Or' in dict.keys():
        for single_filter in dict['Or']:
            if single_filter is not None:
                validate_filter(single_filter, schema)
    else:
        jsonschema.validate(dict, schema)


def sort_dictionary(input):
    res = OrderedDict()

    for k, v in sorted(input.items()):
        if isinstance(v, dict):
            res[k] = sort_dictionary(v)
        elif isinstance(v, list):
            sorted_items = []

            for item in v:
                if isinstance(item, dict):
                    sorted_items.append(sort_dictionary(item))
                else:
                    sorted_items.append(item)

            res[k] = sorted(sorted_items)
        else:
            res[k] = v

    return json.dumps(res)
