import datetime
import json
import urllib

import tornado.web
from pymongo.errors import BulkWriteError
from social.apps.django_app.default.models import UserSocialAuth
from tornado import gen

from ografy import settings
from ografy.apps.passthrough.auth import user_authenticated
from ografy.apps.passthrough.documents import Data, Settings, Signal, motor_connection
from ografy.contrib.estoolbox import SEARCH_TEXT_FIELDS
from ografy.contrib.estoolbox.security import InvalidDSLQueryException, validate_dsl
from ografy.contrib.estoolbox.tornadoes_bulk import ESBulkConnection
from ografy.contrib.locationtoolbox import estimation
from ografy.contrib.pytoolbox import strip_invalid_key_characters


es_connection = ESBulkConnection(
    settings.ELASTICSEARCH['HOST'],
    settings.ELASTICSEARCH['PORT']
)

es_connection.client.max_clients = 1000
es_connection.client.defaults['request_timeout'] = 1000
es_connection.client.defaults['connect_timeout'] = 1000


@gen.coroutine
def bulk_unique_post_and_id_replace(index, type, bulk_document_list, document_unique_id_list, document_id_mapping_dict):
    document_post_response = yield es_connection.bulk_unique_post(index, type, bulk_document_list, document_unique_id_list)
    document_post_response_decoded = json.loads(document_post_response.body.decode('utf-8'))['items']

    for index, document in enumerate(bulk_document_list):
        document_response_item = document_post_response_decoded[index]

        if 'create' in document_response_item.keys():
            document_id_mapping_dict[document['ografy_unique_id']] = document_response_item['create']['_id']
        else:
            document_id_mapping_dict[document['ografy_unique_id']] = document_response_item['index']['_id']


class EventHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def get(self, slug=None):
        limit = json.loads(self.get_argument('limit'))
        offset = json.loads(self.get_argument('offset'))
        filters = json.loads(self.get_argument('filters', default='{"bool":{"must":[],"must_not":[],"should":[]}}'))
        q = self.get_argument('q')

        try:
            validate_dsl(filters)

            query = {
                'query': {
                    'filtered': {
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

            if len(q) > 0:
                query['query']['filtered']['query'] = {
                    'multi_match': {
                        'query': q,
                        'type': 'most_fields',
                        'fields': SEARCH_TEXT_FIELDS
                    }
                }

            index = 'core'
            object_type = 'event'

            response = yield es_connection.search(
                index=index,
                type=object_type,
                source=query
            )

            object_type = 'search'

            cleaned_results = []
            body_decoded = json.loads(response.body.decode('utf-8'))
            result_total = body_decoded['hits']['total']
            results = body_decoded['hits']['hits']

            for result in results:
                cleaned_results.append({'id': result['_id'], 'result': result['_source']})

            search_response = {
                'results': cleaned_results
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
                    'filters': json.dumps(filters)
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
                    'filters': json.dumps(filters)
                })

                next_url = urllib.parse.urlunparse(url_parts)

                search_response['next'] = next_url

            self.write(search_response)

            action_and_metadata = {
                'index': {
                    '_index': index,
                    '_type': object_type
                }
            }

            document = {
                'datetime': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'search_DSL': strip_invalid_key_characters(query),
                'tags': [],
                'user_id': self.request.user.id
            }

            bulk_insert_body = json.dumps(action_and_metadata) + '\n' + json.dumps(document) + '\n'

            yield es_connection.bulk_operation(
                type=object_type,
                index=index,
                body=bulk_insert_body
            )

            self.finish()
        except InvalidDSLQueryException:
            self.send_error(400, mesg='Invalid DSL query. Please check the documentation')

    # Posting Events is a multi-step process that actually involves posting associated Contacts, Content, and Data, and
    # posting every one of these document types requires a uniqueness check so that the same document isn't posted
    # more than once.
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def post(self, slug=None):
        # Each document type needs a few different lists/dictionaries for the insertion process.
        # The bulk list is just a list of all of the documents that are going to be inserted.
        bulk_data_list = []
        # The unique ID list is a list of all the unique IDs of documents that are going to be inserted.
        # It is used to make sure that the same document isn't added more than once.  For example, if a number of
        # Twitter direct messages are from the same person, we only want to attempt to insert that Contact once.
        data_unique_id_list = []
        # The mapping dictionary is used to store the ElasticSearch IDs of documents that are already present
        # in the database.  The keys are unique IDs and the values are ElasticSearch IDs.
        data_id_mapping_dict = {}

        bulk_contact_list = []
        contact_unique_id_list = []
        contact_id_mapping_dict = {}

        bulk_content_list = []
        content_unique_id_list = []
        content_id_mapping_dict = {}

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
            event_data_id_list = []
            event_contacts_list = []
            event_content_list = []

            # Parse each Data object associated with this Event.
            for data in post_event['data_list']:
                # Get the current datetime
                datenow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                # Add the user ID
                data['user_id'] = user_id
                # Set the created and updated fields to the current datetime
                data['created'] = datenow
                data['updated'] = datenow
                # Add the Signal ID
                data['signal'] = post_event['signal']

                # Only add the current Data object's unique ID to the unique ID list if it isn't already present.
                # This is to prevent the same document from being indexed multiple times (more relevant to inserting
                # Content and Contacts, but doesn't hurt to do it for Data as well).
                if data['ografy_unique_id'] not in data_unique_id_list:
                    # Add a copy of the Data object to the global list of all Data being inserted
                    bulk_data_list.append(data.copy())
                    # Add the Data's unique ID to the list of unique IDs of Data being inserted
                    data_unique_id_list.append(data['ografy_unique_id'])

                # Add the Data's unique ID to the list of Data this Event references
                event_data_id_list.append(data['ografy_unique_id'])

            # Parse each Contact object associated with this Event
            for contact in post_event['contacts_list']:
                # Add a copy of the list of Data IDs that are associated with this Event.
                contact['data_id_list'] = event_data_id_list.copy()
                # Add the Signal ID.
                contact['signal'] = post_event['signal']
                # Add the user ID.
                contact['user_id'] = user_id

                # Only add the current Contact object's unique ID to the unique ID list if it isn't already present.
                # This is to prevent the same document from being indexed multiple times.
                if contact['ografy_unique_id'] not in contact_unique_id_list:
                    # Add a copy of the Contact object to the global list of all Contacts being inserted
                    bulk_contact_list.append(contact.copy())
                    # Add the Contact's unique ID to the list of unique IDs of Contacts being inserted
                    contact_unique_id_list.append(contact['ografy_unique_id'])

                # The local copy of the Contact present in the Event does not need the user ID, Signal ID or data ID list
                # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                del contact['user_id']
                del contact['signal']
                del contact['data_id_list']
                # The local copy of the Contact also does not need the unique ID.  It will need the ElasticSearch ID
                # of the entry in the Contact collection, but we don't have that yet since it hasn't been indexed.
                # In the interim, have the ES ID field store the unique ID; once Contacts have been indexed,
                # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                contact['contact'] = contact['ografy_unique_id']
                # Delete the unique ID field
                del contact['ografy_unique_id']

                # Add the local copy of the Contact to the list of Contacts this Event references.
                event_contacts_list.append(contact)

            # Parse each Content object associated with this Event
            for content in post_event['content_list']:
                # Add a copy of the list of Data IDs that are associated with this Event.
                content['data_id_list'] = event_data_id_list.copy()
                # Add the Signal ID.
                content['signal'] = post_event['signal']
                # Add the user ID.
                content['user_id'] = user_id

                # Only add the current Content object's unique ID to the unique ID list if it isn't already present.
                # This is to prevent the same document from being indexed multiple times.
                if content['ografy_unique_id'] not in content_unique_id_list:
                    # Add a copy of the Content object to the global list of all Content being inserted
                    bulk_content_list.append(content.copy())
                    # Add the Content's unique ID to the list of unique IDs of Content being inserted
                    content_unique_id_list.append(content['ografy_unique_id'])

                # The local copy of the Content present in the Event does not need the user ID, Signal ID or data ID list
                # since the Event stores all those fields.  Delete them from the copy being stored on the Event.
                del content['user_id']
                del content['signal']
                del content['data_id_list']
                # The local copy of the Content also does not need the unique ID.  It will need the ElasticSearch ID
                # of the entry in the Content collection, but we don't have that yet since it hasn't been indexed.
                # In the interim, have the ES ID field store the unique ID; once Contents have been indexed,
                # the unique ID will be mapped to the ES ID and we can then replace the unique ID with the ES ID.
                content['content'] = content['ografy_unique_id']
                # Delete the unique ID field
                del content['ografy_unique_id']

                # Add the local copy of the Content to the list of Content this Event references.
                event_content_list.append(content)

            # If the Event did not have something that could be mapped to a Location, that field will be blank.
            # In this case, the Location will need to be estimated.
            if 'location' not in post_event.keys():
                # If the Event did not have a datetime, then use the current datetime.
                if 'datetime' not in post_event.keys():
                    post_event['datetime'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

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

            # Make copies of the lists of documents/IDs that the Event references.
            post_event['contacts_list'] = event_contacts_list.copy()
            post_event['content_list'] = event_content_list.copy()
            post_event['data_id_list'] = event_data_id_list.copy()
            # Add the user ID.
            post_event['user_id'] = user_id
            # Delete the list of full Data objects since it is not needed any more.
            del post_event['data_list']

            # Add the Event object to the global list of all Events being inserted
            bulk_event_list.append(post_event.copy())
            # Add the Event's unique ID to the list of unique IDs of Events being inserted
            event_unique_id_list.append(post_event['ografy_unique_id'])

        # If there is Data to be indexed, then do so.
        # bulk_unique_post_and_id_replace will populate the unique ID list with the necessary key-value relations
        # between unique IDs and ElasticSearch IDs.
        # The callback using gen.Callback allows for us to wait until any point in the code for that to finish before
        # continuing.  It's not really necessary to use this for Data, since nothing else can be done until the Data
        # posting process has completed, but it's in line with the way the other document types are handled.
        if len(bulk_data_list) > 0:
            bulk_unique_post_and_id_replace('core', 'data', bulk_data_list, data_unique_id_list, data_id_mapping_dict, callback=(yield gen.Callback('data_bulk_unique_post_and_id_replace')))

            # This holds up this entire method until the Data has been uniquely indexed.
            yield gen.Wait('data_bulk_unique_post_and_id_replace')

            bulk = motor_connection.data.initialize_unordered_bulk_op()

            for data in bulk_data_list:
                data['_id'] = data_id_mapping_dict[data['ografy_unique_id']]
                bulk.insert(data)

            bulk.execute(callback=(yield gen.Callback('mongo_data_insert')))

        # Now that the Data is indexed, the ID mapping dictionary has key-value relations between the unique IDs
        # and the ElasticSearch IDs of the Data documents corresponding to those unique IDs.
        # Use this to replace all of the unique IDs in every Contact with its associated ES ID.
        for contact in bulk_contact_list:
            for index, data in enumerate(contact['data_id_list']):
                contact['data_id_list'][index] = data_id_mapping_dict[data]

        # Now that the Data is indexed, the ID mapping dictionary has key-value relations between the unique IDs
        # and the ElasticSearch IDs of the Data documents corresponding to those unique IDs.
        # Use this to replace all of the unique IDs in every Content with its associated ES ID.
        for content in bulk_content_list:
            for index, data in enumerate(content['data_id_list']):
                content['data_id_list'][index] = data_id_mapping_dict[data]

        # If there are Contacts or Content to be indexed, then do so.
        # bulk_unique_post_and_id_replace will populate the unique ID list with the necessary key-value relations
        # between unique IDs and ElasticSearch IDs.
        # The callback using gen.Callback allows for us to wait until any point in the code for that to finish before
        # continuing, and allows for multiple asynchronous functions to be run simultaneously while still waiting for
        # all to finish before proceeding.
        if len(bulk_contact_list) > 0:
            bulk_unique_post_and_id_replace('core', 'contact', bulk_contact_list, contact_unique_id_list, contact_id_mapping_dict, callback=(yield gen.Callback('contact_bulk_unique_post_and_id_replace')))
        if len(bulk_content_list) > 0:
            bulk_unique_post_and_id_replace('core', 'content', bulk_content_list, content_unique_id_list, content_id_mapping_dict, callback=(yield gen.Callback('content_bulk_unique_post_and_id_replace')))

        # These wait for the Contact bulk unique post and the Content bulk post to finish, but in each case only if there
        # were any of that document type to post.
        # This is structured so that both operations can run at the same time, rather than doing the Contact bulk post
        # and waiting for it to finish before doing the Content bulk post.  The Event bulk posting will not occur until
        # both of those operations are complete (or just one if only one needs to be run; if neither need to be run,
        # then this would be skipped entirely).
        if len(bulk_contact_list) > 0:
            yield gen.Wait('contact_bulk_unique_post_and_id_replace')
        if len(bulk_content_list) > 0:
            yield gen.Wait('content_bulk_unique_post_and_id_replace')

        # Now that the Contacts and Contents are indexed, as well as the Data that had been completed prior to those two,
        # the ID mapping dictionary has key-value relations between the unique IDs of each associated document
        # and the ElasticSearch IDs of the Data, Contact, and Content documents corresponding to those unique IDs.
        # Use these mapping dictionaries to replace all of the unique IDs in every Event with the associated ES ID.
        for event in bulk_event_list:
            for index, data in enumerate(event['data_id_list']):
                event['data_id_list'][index] = data_id_mapping_dict[data]

            for contact in event['contacts_list']:
                contact['contact'] = contact_id_mapping_dict[contact['contact']]

            for content in event['content_list']:
                content['content'] = content_id_mapping_dict[content['content']]

        # Post the Events.  There's no need to use the ID replacement version of bulk_unique_post since nothing
        # references the Events and thus there's no need to save the unique ID as a placeholder for an ES ID.
        event_post_response = yield es_connection.bulk_unique_post('core', 'event', bulk_event_list, event_unique_id_list)
        # Decode the response so that it can be sent back to the client that made the call.
        event_post_response_decoded = json.loads(event_post_response.body.decode('utf-8'))

        try:
            yield gen.Wait('mongo_data_insert')
            pass
        except BulkWriteError as err:
            pass

        self.write(event_post_response_decoded)
        self.finish()

    @tornado.web.asynchronous
    def options(self):
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
    @user_authenticated
    @gen.coroutine
    def delete(self, slug=None):
        user_id = self.request.user.id

        delete_user_documents('location', user_id)

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self, slug=None):
        user_id = self.request.user.id

        delete_user_documents('search', user_id)

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
        new_estimate_allowed = datetime.datetime.now() > next_estimate_date

        if (new_estimate_allowed):
            estimation.reestimate_all(self.request.user.id)

            self.set_status(200, 'Re-estimation successful.')
        else:
            self.set_status(400, 'Re-estimation not allowed yet.')

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class SignalHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self, slug=None):
        user_id = self.request.user.id
        signal_id_to_delete = self.get_argument('signal_id')

        delete_signal_and_linked_documents(signal_id_to_delete, user_id)

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


class AccountHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @user_authenticated
    @gen.coroutine
    def delete(self, slug=None):
        user = self.request.user
        user_id = user.id

        Settings.objects.filter(user_id=user_id).delete()
        signals = Signal.objects.filter(user_id=user_id).find_all(callback=(yield gen.Callback('signal_get')))
        Data.objects.filter(user_id=user_id).delete()

        UserSocialAuth.objects.filter(user=user).delete()

        delete_user_documents('search', user_id)
        delete_user_documents('location', user_id)

        yield gen.Wait('signal_get')

        for signal in signals:
            delete_signal_and_linked_documents(str(signal._id), user_id)

        user.delete()

        self.finish()

    @tornado.web.asynchronous
    def options(self):
        self.finish()


@gen.coroutine
def delete_signal_and_linked_documents(signal_id, user_id):
    signal_to_delete = yield Signal.objects.get(id=signal_id, user_id=user_id)
    index = 'core'

    terms = {
        'user_id': user_id,
        'signal': signal_id
    }

    for type in ['data', 'contact', 'content', 'event']:
        es_connection.bulk_delete(index, type, terms)

    yield signal_to_delete.delete()


@gen.coroutine
def delete_user_documents(doc_type, user_id):
    index = 'core'

    terms = {
        'user_id': user_id
    }

    es_connection.bulk_delete(index, doc_type, terms)
