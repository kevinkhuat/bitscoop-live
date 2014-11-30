from datetime import datetime
import requests

from django.test import SimpleTestCase
from django.core import serializers
from django.http import HttpResponse
from mongoengine.queryset.queryset import QuerySet

from ografy.apps.obase import api as ObaseApi
from ografy.apps.obase.documents import Message, Data, Event
from ografy.apps.obase.models import Provider, Signal
from ografy.apps.xauth.models import User


class TestOBase(SimpleTestCase):
    fixtures = []

    # def test_OBase_Signal_Api(self):
    #     test_user = User(email='test@test.test', handle='testy')
    #     test_user.save()
    #     test_provider = ObaseApi.Provider.get(val=1)
    #     test_signal = ObaseApi.Signal.post(name='Facebook', provider=test_provider, user=test_user)
    #     test_json = serializers.serialize("json", test_signal)

    def test_OBase_Data(self):

        # Create initial test data for testing POST
        test_time = datetime.now()
        test_data = {
            'created': test_time,
            'updated': test_time,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        # POST the data, save the ID, then GET the data back and check
        # that the 'data_blob' field is correct, which indicates the POST was successful
        posted_data = ObaseApi.Data.post(test_data)
        data_id = posted_data.id
        get_data_from_db = ObaseApi.Data.get(data_id)
        self.assertEqual(get_data_from_db.data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])


        # Create new test data for testing PUT
        # This data is not the same as the POST test data
        test_time = datetime(2011, 5, 15, 15, 12, 40)
        test_data = {
            'created': test_time,
            'updated': test_time,
            'data_blob': ["{'top': 'dog'}"]
        }

        # PUT the new data in over the old data
        # Don't need to save the ID again since it hasn't changed
        # GET the data back and check that it has been overwritten correctly
        # Check both the 'data_blob' and created fields to ensure this
        put_get_data_from_db = ObaseApi.Data.put(data_id, test_data)
        get_data_from_db = ObaseApi.Data.get(data_id)
        self.assertEqual(get_data_from_db.data_blob, ["{'top': 'dog'}"])
        self.assertEqual(get_data_from_db.created, test_time)


        # Create new test data for testing PATCH
        # 'test_time' will be changed but will not be patched in to make sure
        # that this variable isn't giving false results
        # Only the new 'data_blob' will be patched in
        test_time = datetime.now()
        test_data['data_blob'] = ["{'hot': 'dog'}"]

        # PATCH the new 'data_blob' in over the old data
        # GET the data back and check that 'data_blob'
        # has been overwitten correctly and that 'created'
        # hasn't changed
        patch_get_data_from_db = ObaseApi.Data.patch(data_id, test_data)
        get_data_from_db = ObaseApi.Data.get(data_id)
        self.assertEqual(get_data_from_db.data_blob, ["{'hot': 'dog'}"])
        self.assertEqual(get_data_from_db.created, datetime(2011, 5, 15, 15, 12, 40))


        # DELETE the entry and check that the response is True,
        # which means the request was successful
        self.assertTrue(ObaseApi.Data.delete(data_id))


        # Test the group GET function
        # It should return an object of type 'QuerySet'
        # and that object's length should be more than 0
        data_list_from_group = list(ObaseApi.Data.get())
        self.assertIsInstance(data_list_from_group, list)
        self.assertIsInstance(data_list_from_group[0], Data)

    def test_OBase_Event(self):

        # Create initial test data for testing POST
        test_time = datetime.now()
        test_data = {
            'created': test_time,
            'updated': test_time,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        # POST the data and save the ID
        posted_data = ObaseApi.Data.post(test_data)
        data_id = posted_data.id

        # Create initial test Event field data
        test_event_fields = {
            'created': test_time,
            'updated': test_time,
            'datetime': test_time,
            'user_id': 1138,
            'provider_id': 10591,
            'signal_id': 1812,
            'provider_name': 'TwitFace',
            'data': data_id,
            # 'location':
        }

        # POST the Event, save the ID, then GET the Event back and check
        # that some fields are correct, which indicates the POST was successful
        posted_event_from_db = ObaseApi.Event.post(test_event_fields)
        event_id = posted_event_from_db.id
        get_event_from_db = ObaseApi.Event.get(event_id)
        self.assertEqual(get_event_from_db['user_id'], 1138)
        self.assertEqual(get_event_from_db['provider_name'], 'TwitFace')
        self.assertEqual(ObaseApi.Data.get(get_event_from_db.data.id).data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])


        # Create new Event field data for the PUT test
        test_event_fields['updated'] = test_time
        test_event_fields['provider_id'] = 92606

        # Test Event PUT by running it and checking that the new field data is returned,
        # Data should be the same since it isn't changed
        put_event_from_db = ObaseApi.Event.put(event_id, test_event_fields)
        self.assertEqual(put_event_from_db.updated, test_time)
        self.assertNotEqual(put_event_from_db.updated, get_event_from_db.created)
        self.assertEqual(put_event_from_db['provider_id'], 92606)
        self.assertEqual(ObaseApi.Data.get(put_event_from_db.data.id).data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])


        # Create new Event field data for the PATCH test
        test_event_fields['provider_name'] = 'FaceTwit'

        # Test Event PATCH by running it and checking that the new field data is returned,
        # Also check that some old data hasn't changed
        patch_event_from_db = ObaseApi.Event.patch(event_id, test_event_fields)
        self.assertEqual(patch_event_from_db['provider_name'], 'FaceTwit')
        self.assertEqual(patch_event_from_db['provider_id'], 92606)
        self.assertEqual(ObaseApi.Data.get(get_event_from_db.data), ["{'cool': 'pants', 'hammer': 'time'}"])


        # DELETE the Event and check that the response is True,
        # which means the request was successful
        self.assertTrue(ObaseApi.Event.delete(data_id))


        # Test the group GET function
        # It should return an object of type 'QuerySet'
        # and that object's length should be more than 0
        event_list_from_group = list(ObaseApi.Event.get())
        self.assertIsInstance(event_list_from_group, list)
        self.assertIsInsatance(event_list_from_group[0], Event)
