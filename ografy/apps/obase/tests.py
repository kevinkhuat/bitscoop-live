from datetime import datetime
import json
import requests

from django.test import SimpleTestCase, TransactionTestCase
from django.http import HttpResponse
from mongoengine.queryset.queryset import QuerySet

from ografy.apps.obase.documents import Data, Event, Message
import ografy.apps.obase.views as ObjectViews
import ografy.apps.obase.api as ObaseApi


class TestOBase(TransactionTestCase):
    fixtures = []

    def test_OBase_Data(self):

        #Create initial test data for testing POST
        testTime = datetime.now()
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        #POST the data, save the ID, then GET the data back and check
        #that the 'data_blob' field is correct, which indicates the POST was successful
        postedData = ObaseApi.Data.post(testData)
        dataId = postedData.id
        gotData = ObaseApi.Data.get(dataId)
        assert (gotData.data_blob == ["{'cool': 'pants', 'hammer': 'time'}"])

        #Create new test data for testing PUT
        #This data is not the same as the POST test data
        testTime = datetime(2011, 5, 15, 15, 12, 40)
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'top': 'dog'}"]
        }

        #PUT the new data in over the old data
        #Don't need to save the ID again since it hasn't changed
        #GET the data back and check that it has been overwritten correctly
        #Check both the 'data_blob' and created fields to ensure this
        putData = ObaseApi.Data.put(dataId, testData)
        gotData = ObaseApi.Data.get(dataId)
        assert(gotData.data_blob == ["{'top': 'dog'}"])
        assert(gotData.created == testTime)

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
        gotData = ObaseApi.Data.get(dataId)
        assert(gotData.data_blob == ["{'hot': 'dog'}"])
        assert(gotData.created == datetime(2011, 5, 15, 15, 12, 40))

        #DELETE the entry and check that the response is True,
        #which means the request was successful
        deleteData = ObaseApi.Data.delete(dataId)
        assert(deleteData == True)


        #Test the group GET function
        #It should return an object of type 'QuerySet'
        #and that object's length should be more than 0
        getGroupData = ObaseApi.Data.get()
        assert(type(getGroupData) is QuerySet)
        assert(len(getGroupData._result_cache) > 0)

        return HttpResponse(True)


    def test_OBase_Event(self):

        #Create initial test data for testing POST
        testTime = datetime.now()
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        }

        testEvent = {
            'created': testTime,
            'updated': testTime,
            'datetime': testTime,
            'user_id': 1138,
            'provider_id': 10591,
            'signal_id': 1812,
            'provider_name': 'TwitFace',
            'data': testData,
            # 'location':
        }

        #POST the data, save the ID, then GET the data back and check
        #that some fields are correct, which indicates the POST was successful
        postedData = ObaseApi.Event.post(testEvent)
        dataId = postedData.id
        gotData = ObaseApi.Data.get(dataId)
        assert (gotData.data.data_blob == ["{'cool': 'pants', 'hammer': 'time'}"])

        #Create new test data for testing PUT
        #This data is not the same as the POST test data
        testTime = datetime(2011, 5, 15, 15, 12, 40)
        testData = {
            'created': testTime,
            'updated': testTime,
            'data_blob': ["{'top': 'dog'}"]
        }

        #PUT the new data in over the old data
        #Don't need to save the ID again since it hasn't changed
        #GET the data back and check that it has been overwritten correctly
        #Check both the 'data_blob' and created fields to ensure this
        putData = ObaseApi.Data.put(dataId, testData)
        gotData = ObaseApi.Data.get(dataId)
        assert(gotData.data_blob == ["{'top': 'dog'}"])
        assert(gotData.created == testTime)

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
        gotData = ObaseApi.Data.get(dataId)
        assert(gotData.data_blob == ["{'hot': 'dog'}"])
        assert(gotData.created == datetime(2011, 5, 15, 15, 12, 40))

        #DELETE the entry and check that the response is True,
        #which means the request was successful
        deleteData = ObaseApi.Data.delete(dataId)
        assert(deleteData == True)


        #Test the group GET function
        #It should return an object of type 'QuerySet'
        #and that object's length should be more than 0
        getGroupData = ObaseApi.Data.get()
        assert(type(getGroupData) is QuerySet)
        assert(len(getGroupData._result_cache) > 0)

        return HttpResponse(True)
