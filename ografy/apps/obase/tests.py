from datetime import datetime
import json
import requests

from django.test import SimpleTestCase, TransactionTestCase
from django.core import serializers
from django.http import HttpResponse
from mongoengine.queryset.queryset import QuerySet

from ografy.apps.obase import api as ObaseApi
from ografy.apps.obase.documents import Message, Data, Event
from ografy.apps.obase.models import Provider, Signal
from ografy.apps.xauth.models import User


class TestOBase(SimpleTestCase):
    fixtures = []

    def test_OBase_Signal_Api(self):
        test_user = User(email='test@test.test', handle='testy')
        test_user.save()
        test_signal = ObaseApi.Signal.post(name='Facebook', backend_name='facebook', user=test_user)
        test_json = serializers.serialize("json", test_signal)

    def test_OBase_Data(self):

        # Create initial test data for testing POST
        testTime = datetime.now()
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        # POST the data, save the ID, then GET the data back and check
        # that the 'data_blob' field is correct, which indicates the POST was successful
        postedData = ObaseApi.Data.post(testData)
        dataId = postedData.id
        getData = ObaseApi.Data.get(dataId)
        assert (getData.data_blob == ["{'cool': 'pants', 'hammer': 'time'}"])


        #Create new test data for testing PUT
        #This data is not the same as the POST test data
        testTime = datetime(2011, 5, 15, 15, 12, 40)
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'top': 'dog'}"]
        }

        # PUT the new data in over the old data
        # Don't need to save the ID again since it hasn't changed
        # GET the data back and check that it has been overwritten correctly
        # Check both the 'data_blob' and created fields to ensure this
        putData = ObaseApi.Data.put(dataId, testData)
        getData = ObaseApi.Data.get(dataId)
        assert(getData.data_blob == ["{'top': 'dog'}"])
        assert(getData.created == testTime)


        #Create new test data for testing PATCH
        #'testTime' will be changed but will not be patched in to make sure
        #that this variable isn't giving false results
        #Only the new 'data_blob' will be patched in
        testTime = datetime.now()
        testData['data_blob'] = ["{'hot': 'dog'}"]

        #PATCH the new 'data_blob' in over the old data
        #GET the data back and check that 'data_blob'
        #has been overwitten correctly and that 'created'
        #hasn't changed
        patchData = ObaseApi.Data.patch(dataId, testData)
        getData = ObaseApi.Data.get(dataId)
        assert(getData.data_blob == ["{'hot': 'dog'}"])
        assert(getData.created == datetime(2011, 5, 15, 15, 12, 40))


        #DELETE the entry and check that the response is True,
        #which means the request was successful
        deleteData = ObaseApi.Data.delete(dataId)
        assert(deleteData == True)


        #Test the group GET function
        #It should return an object of type 'QuerySet'
        #and that object's length should be more than 0
        getGroupData = ObaseApi.Data.get()
        assert isinstance(getGroupData, QuerySet)
        assert isinstance(getGroupData._result_cache[0], Data)
        assert (len(getGroupData._result_cache) > 0)

        return HttpResponse(True)


    def test_OBase_Event(self):

        #Create initial test data for testing POST
        testTime = datetime.now()
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        #POST the data and save the ID
        postedData = ObaseApi.Data.post(testData)
        dataId = postedData.id

        #Create initial test Event field data
        testEvent = {
            'created': testTime,
            'updated': testTime,
            'datetime': testTime,
            'user_id': 1138,
            'provider_id': 10591,
            'signal_id': 1812,
            'provider_name': 'TwitFace',
            'data': postedData.id,
            # 'location':
        }

        #POST the Event, save the ID, then GET the Event back and check
        #that some fields are correct, which indicates the POST was successful
        postedEvent = ObaseApi.Event.post(testEvent)
        eventId = postedEvent.id
        getEvent = ObaseApi.Event.get(eventId)
        assert(getEvent['user_id'] == 1138)
        assert(getEvent['provider_name'] == 'TwitFace')
        assert(ObaseApi.Data.get(getEvent.data) == ["{'cool': 'pants', 'hammer': 'time'}"])


        #Create new Event field data for the PUT test
        testEvent['updated'] = testTime
        testEvent['provider_id'] = 92606

        #Test Event PUT by running it and checking that the new field data is returned,
        #Data should be the same since it isn't changed
        putEvent = ObaseApi.Event.put(eventId, testEvent)
        assert(getEvent.updated == testTime)
        assert(getEvent.updated != getEvent.created)
        assert(getEvent['provider_id'] == 92606)
        assert(ObaseApi.Data.get(getEvent.data) == ["{'cool': 'pants', 'hammer': 'time'}"])


        #Create new Event field data for the PATCH test
        testEvent['provider_name'] = 'FaceTwit'

        #Test Event PATCH by running it and checking that the new field data is returned,
        #Also check that some old data hasn't changed
        patchEvent = ObaseApi.Event.patch(eventId, testEvent)
        assert(patchEvent['provider_name'] == 'FaceTwit')
        assert(patchEvent['provider_id'] == 92606)
        assert(ObaseApi.Data.get(getEvent.data) == ["{'cool': 'pants', 'hammer': 'time'}"])


        #DELETE the Event and check that the response is True,
        #which means the request was successful
        deleteData = ObaseApi.Event.delete(dataId)
        assert(deleteData == True)


        #Test the group GET function
        #It should return an object of type 'QuerySet'
        #and that object's length should be more than 0
        getGroupEvent = ObaseApi.Event.get()
        assert(type(getGroupEvent) is QuerySet)
        assert(len(getGroupEvent._result_cache) > 0)

        return HttpResponse(True)
