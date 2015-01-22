from datetime import datetime

from django.test import SimpleTestCase

from ografy.apps.obase import api as ObaseApi
from ografy.apps.obase.documents import Data

# TODO: Get from settings
BASE_URL = 'dev.ografy.io'


class TestoBase(SimpleTestCase):
    # def test_OBase_Signal_Api(self):
    # test_user = User(email='test@test.test', handle='testy')
    # test_user.save()
    # test_provider = ObaseApi.Provider.get(val=1)
    # test_signal = ObaseApi.Signal.post(name='Facebook', provider=test_provider, user=test_user)
    # test_json = serializers.serialize("json", test_signal)

    # def test_Data(self):
    #
    #     # Create initial test data for testing POST
    #     test_time = datetime.now()
    #     test_data = {
    #         'created': test_time,
    #         'updated': test_time,
    #         'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
    #     }
    #
    #     # POST the data, save the ID, then GET the data back and check
    #     # that the 'data_blob' field is correct, which indicates the POST was successful
    #     post_data_from_db = ObaseApi.Data.post(test_data)
    #     data_id = post_data_from_db.id
    #     get_data_from_db = ObaseApi.Data.get(data_id)
    #     self.assertEqual(get_data_from_db.data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])
    #     self.assertEqual(post_data_from_db, get_data_from_db)
    #
    #     # Create new test data for testing PUT
    #     # This data is not the same as the POST test data
    #     test_time = datetime(2011, 5, 15, 15, 12, 40)
    #     test_data = {
    #         'created': test_time,
    #         'updated': test_time,
    #         'data_blob': ["{'top': 'dog'}"]
    #     }
    #
    #     # PUT the new data in over the old data
    #     # Don't need to save the ID again since it hasn't changed
    #     # GET the data back and check that it has been overwritten correctly
    #     # Check both the 'data_blob' and created fields to ensure this
    #     put_data_from_db = ObaseApi.Data.put(data_id, test_data)
    #     get_data_from_db = ObaseApi.Data.get(data_id)
    #     self.assertEqual(get_data_from_db.data_blob, ["{'top': 'dog'}"])
    #     self.assertEqual(get_data_from_db.created, test_time)
    #     self.assertEqual(put_data_from_db, get_data_from_db)
    #
    #     # Create new test data for testing PATCH
    #     # 'test_time' will be changed but will not be patched in to make sure
    #     # that this variable isn't giving false results
    #     # Only the new 'data_blob' will be patched in
    #     test_time = datetime.now()
    #     test_data['data_blob'] = ["{'hot': 'dog'}"]
    #
    #     # PATCH the new 'data_blob' in over the old data
    #     # GET the data back and check that 'data_blob'
    #     # has been overwitten correctly and that 'created'
    #     # hasn't changed
    #     patch_data_from_db = ObaseApi.Data.patch(data_id, {'data_blob': test_data['data_blob']})
    #     get_data_from_db = ObaseApi.Data.get(data_id)
    #     self.assertEqual(get_data_from_db.data_blob, ["{'hot': 'dog'}"])
    #     self.assertEqual(get_data_from_db.created, datetime(2011, 5, 15, 15, 12, 40))
    #     self.assertEqual(patch_data_from_db, get_data_from_db)
    #
    #
    #     # DELETE the entry and check that the response is True,
    #     # which means the request was successful
    #     self.assertTrue(ObaseApi.Data.delete(data_id))
    #
    #
    #     # Test the group GET function
    #     # It should return an object of type 'QuerySet'
    #     # and that object's length should be more than 0
    #     data_list_from_group = list(ObaseApi.Data.get())
    #     self.assertIsInstance(data_list_from_group, list)
    #     self.assertIsInstance(data_list_from_group[0], Data)

    # def test_ProviderGroupView(self):
    #     provider_list = requests.get(BASE_URL + '/obase/provider')
    #     pass

    # def test_DataGroupView(self):
    #
    #     dj = jsonizer.DataJsonizer()
    #     # Test Post
    #
    #     current_test_time = datetime.now()
    #     post_test_data_1 = Data(
    #         created = current_test_time,
    #         updated = current_test_time,
    #         data_blob = ["{'wonder': 'bread', 'mega': 'man'}"]
    #     )
    #
    #     post_test_data_2 = Data(
    #         created = current_test_time,
    #         updated = current_test_time,
    #         data_blob = ["{'can': 'can'}"]
    #     )
    #
    #     post_test_data_list = []
    #
    #     post_test_data_list.append(post_test_data_1)
    #     post_test_data_list.append(post_test_data_2)
    #
    #     post_json_data_list = dj.serialize_list(post_test_data_list)
    #     post_url = reverse('obase_group_data')
    #     post_return_response = self.client.post(post_url, json=post_json_data_list, content_type="application/json", HTTP_USER_AGENT='Mozilla/5.0')
    #
    #     # Test Get
    #
    #     # Add some data using the internal API
    #
    #     get_return_response = self.client.get(post_url, HTTP_USER_AGENT='Mozilla/5.0')
    #     # get_response_data = dj.deserialize_list(get_return_response.content.decode('utf-8'))
    #
    #     data = dj.deserialize_list(get_response_data)
    #
    #     self.assertIsInstance(data, Data)

    def test_DataSingleView(self):
        # jj = jsonizer.Jsonizer()
        # bj = jsonizer.BsonJsonizer()
        # dj = jsonizer.DataJsonizer()
        #
        current_test_time = datetime.now()
        fixed_test_time = datetime(2011, 5, 15, 15, 12, 40)

        post_test_data = Data(
            created=current_test_time,
            updated=current_test_time,
            data_blob=["{'wonder': 'bread', 'mega': 'man'}"]
        )

        ObaseApi.DataApi.post(post_test_data)
        #
        # json_test_data = dj.serialize(post_test_data)
        #
        # post_url = reverse('obase_group_data')
        # post_return_response = self.client.post(post_url, data=json_test_data, content_type="application/json",  HTTP_USER_AGENT='Mozilla/5.0')
        #
        # post_response_data = dj.deserialize(post_return_response.content.decode('utf-8'))
        # post_return_data_id = bj.get_serialized_value(post_response_data.id, "$oid")
        #
        # get_url = reverse('obase_single_data', kwargs={'id': post_return_data_id})
        # get_return_response = self.client.get(get_url, HTTP_USER_AGENT='Mozilla/5.0')
        #
        # get_response_data = dj.deserialize(get_return_response.content.decode('utf-8'))
        #
        # self.assertEqual(get_response_data.id, post_response_data.id)
        # self.assertEqual(get_response_data.pk, post_response_data.pk)
        # self.assertEqual(get_response_data.created, post_response_data.created)
        # self.assertEqual(get_response_data.updated, post_response_data.updated)
        # self.assertEqual(get_response_data.data_blob, post_response_data.data_blob)
        #
        #
        # put_data_id = post_return_data_id
        # put_test_data = {
        #     'id': put_data_id,
        #     'created': fixed_test_time,
        #     'updated': fixed_test_time,
        #     'data_blob': ["{'chocolate milk': 'amazing'}"]
        # }
        #
        # json_test_data = jj.serialize(put_test_data)
        #
        # put_url = reverse('obase_single_data', kwargs={'id': put_data_id})
        # put_return_response = self.client.put(put_url, data=json_test_data, content_type="application/json",  HTTP_USER_AGENT='Mozilla/5.0')
        #
        # put_response_data = dj.deserialize(put_return_response.content.decode('utf-8'))
        # put_return_data_id = bj.get_serialized_value(put_response_data.id, "$oid")
        #
        # get_url = reverse('obase_single_data', kwargs={'id': put_return_data_id})
        # get_return_response = self.client.get(get_url, HTTP_USER_AGENT='Mozilla/5.0')
        #
        # get_response_data = dj.deserialize(get_return_response.content.decode('utf-8'))
        #
        # self.assertEqual(get_response_data.id, put_response_data.id)
        # self.assertEqual(get_response_data.pk, put_response_data.pk)
        # self.assertEqual(get_response_data.created, put_response_data.created)
        # self.assertEqual(get_response_data.updated, put_response_data.updated)
        # self.assertEqual(get_response_data.data_blob, put_response_data.data_blob)

        # put_return = requests.put(BASE_URL + '/obase/data/' + data_id, data=json_data, verify=False)
        #
        # get_return = requests.get(BASE_URL + '/obase/data' + data_id, verify=False)
        # get_return_json = get_return.GET
        # get_data = dj.deserialize(get_return_json)
        # self.assertEqual(get_data, test_data)
        #
        # test_data.created = datetime.now()
        #
        # json_data = dj.serialize(test_data)
        # patch_return = requests.patch(BASE_URL + 'obase/data' + data_id, data= test_data.created, verify=False)
        #
        # get_return = requests.get(BASE_URL + '/obase/data' + data_id, verify=False)
        # get_return_json = get_return.GET
        # get_data = dj.deserialize(get_return_json)
        # self.assertEqual(get_data, test_data)
        #
        # delete_return = requests.delete(BASE_URL + 'obase/data' + data_id, verify=False)
        # self.assertTrue(delete_return)

        # def test_EventGroupView(self):
        #     # Test Post
        #
        #     test_time = datetime.now()
        #     test_data_1 = Data(
        #         created = test_time,
        #         updated = test_time,
        #         data_blob = ["{'wonder': 'bread', 'mega': 'man'}"]
        #     )
        #
        #     test_data_2 = Data(
        #         created = test_time,
        #         updated = test_time,
        #         data_blob = ["{'can': 'can'}"]
        #     )
        #
        #     data_list = []
        #
        #     data_jsonizer = jsonizer.DataJsonizer()
        #     data_list.append(test_data_1)
        #     data_list.append(test_data_2)
        #
        #     json_data_list = data_jsonizer.serialize_list(data_list)
        #     post_request = requests.post(BASE_URL + '/obase/data/post', json=json_data_list, verify=False)
        #
        #     data_id_1 = post_request['id']
        #     data_id_2 = post_request['id']
        #
        #
        #     test_event_1 = Event(
        #         created = test_time,
        #         updated = test_time,
        #         user_id = 1138,
        #         signal_id = 10101,
        #         provider_id = 1812,
        #         provider_name = 'Twitbook',
        #         datetime = test_time,
        #         data = data_id_1
        #     )
        #
        #     test_event_2 = Event(
        #         created = test_time,
        #         updated = test_time,
        #         user_id = 1138,
        #         signal_id = 10101,
        #         provider_id = 1812,
        #         provider_name = 'Twitbook',
        #         datetime = test_time,
        #         data = data_id_2
        #     )
        #
        #     event_list = []
        #     event_jsonizer = jsonizer.EventJsonizer()
        #
        #     event_list.append(test_event_1)
        #     event_list.append(test_event_2)
        #
        #     json_event_list = event_jsonizer.serialize_list(event_list)
        #     post_request = requests.post(BASE_URL + '/obase/data/event', json=json_event_list, verify=False)
        #
        #
        #     # Test Get
        #
        #     # Add some data using the internal API
        #
        #     request = requests.get(BASE_URL + '/obase/event/', verify=False)
        #     get_return_json = request.GET
        #
        #     event = event_jsonizer.deserialize(get_return_json)
        #
        #     self.assertEqual(event, {})
        #
        # def test_EventSingleView(self):
        #     test_time = datetime.now()
        #     test_data = Data(
        #         created = test_time,
        #         updated = test_time,
        #         data_blob = ["{'wonder': 'bread', 'mega': 'man'}"]
        #     )
        #
        #     data_jsonizer = jsonizer.DataJsonizer()
        #
        #     json_data = data_jsonizer.serialize(test_data)
        #
        #     post_return = requests.post(BASE_URL + '/obase/data/', json=json_data, verify=False)
        #
        #     data_id = post_return.DATA['id']
        #     get_return = requests.get(BASE_URL + '/obase/data/' + data_id)
        #     get_return_json = get_return.GET
        #     get_data = data_jsonizer.deserialize(get_return_json)
        #     self.assertEqual(get_data, test_data)
        #
        #     fixed_time = datetime(2011, 5, 15, 15, 12, 40)
        #     test_data = Data(
        #         created = fixed_time,
        #         updated = fixed_time,
        #         data_blob = ["{'chocolate milk': 'amazing'}"]
        #     )
        #
        #     json_data = data_jsonizer.serialize(test_data)
        #     put_return = requests.put(BASE_URL + '/obase/data/' + data_id, data=json_data, verify=False)
        #
        #     get_return = requests.get(BASE_URL + '/obase/data' + data_id, verify=False)
        #     get_return_json = get_return.GET
        #     get_data = data_jsonizer.deserialize(get_return_json)
        #     self.assertEqual(get_data, test_data)
        #
        #     test_data.created = datetime.now()
        #
        #     json_data = data_jsonizer.serialize(test_data)
        #     patch_return = requests.patch(BASE_URL + 'obase/data' + data_id, data= test_data.created, verify=False)
        #
        #     get_return = requests.get(BASE_URL + '/obase/data' + data_id, verify=False)
        #     get_return_json = get_return.GET
        #     get_data = data_jsonizer.deserialize(get_return_json)
        #     self.assertEqual(get_data, test_data)
        #
        #     delete_return = requests.delete(BASE_URL + 'obase/data' + data_id, verify=False)
        #     self.assertTrue(delete_return)
        #
        # def test_Event(self):
        #
        #     # Create initial test data for testing POST
        #     test_time = datetime.now()
        #     test_data = {
        #         'created': test_time,
        #         'updated': test_time,
        #         'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        #     }
        #
        #     # POST the data and save the ID
        #     posted_data = ObaseApi.Data.post(test_data)
        #     data_id = posted_data.id
        #
        #     # Create initial test Event field data
        #     test_event_fields = {
        #         'created': test_time,
        #         'updated': test_time,
        #         'datetime': test_time,
        #         'user_id': 1138,
        #         'provider_id': 10591,
        #         'signal_id': 1812,
        #         'provider_name': 'TwitFace',
        #         'data': data_id,
        #         # 'location':
        #     }
        #
        #     # POST the Event, save the ID, then GET the Event back and check
        #     # that some fields are correct, which indicates the POST was successful
        #     posted_event_from_db = ObaseApi.Event.post(test_event_fields)
        #     event_id = posted_event_from_db.id
        #     get_event_from_db = ObaseApi.Event.get(event_id)
        #     self.assertEqual(get_event_from_db['user_id'], 1138)
        #     self.assertEqual(get_event_from_db['provider_name'], 'TwitFace')
        #     self.assertEqual(ObaseApi.Data.get(get_event_from_db.data.id).data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])
        #     self.assertEqual(posted_event_from_db, get_event_from_db)
        #
        #
        #     # Create new Event field data for the PUT test
        #     test_event_fields['updated'] = test_time
        #     test_event_fields['provider_id'] = 92606
        #
        #     # Test Event PUT by running it and checking that the new field data is returned,
        #     # Data should be the same since it isn't changed
        #     put_event_from_db = ObaseApi.Event.put(event_id, test_event_fields)
        #     self.assertEqual(put_event_from_db.updated, test_time)
        #     self.assertNotEqual(put_event_from_db.updated, get_event_from_db.created)
        #     self.assertEqual(put_event_from_db['provider_id'], 92606)
        #     self.assertEqual(ObaseApi.Data.get(put_event_from_db.data.id).data_blob, ["{'cool': 'pants', 'hammer': 'time'}"])
        #     self.assertEqual(put_event_from_db, get_event_from_db)
        #
        #     # Create new Event field data for the PATCH test
        #     test_event_fields['provider_name'] = 'FaceTwit'
        #
        #     # Test Event PATCH by running it and checking that the new field data is returned,
        #     # Also check that some old data hasn't changed
        #     patch_event_from_db = ObaseApi.Event.patch(event_id, {'provider_name': test_event_fields['provider_name']})
        #     self.assertEqual(patch_event_from_db['provider_name'], 'FaceTwit')
        #     self.assertEqual(patch_event_from_db['provider_id'], 92606)
        #     self.assertEqual(ObaseApi.Data.get(get_event_from_db.data.id)['data_blob'], ["{'cool': 'pants', 'hammer': 'time'}"])
        #     self.assertEqual(patch_event_from_db, get_event_from_db)
        #
        #     # DELETE the Event and check that the response is True,
        #     # which means the request was successful
        #     self.assertTrue(ObaseApi.Event.delete(event_id))
        #     self.assertTrue(ObaseApi.Data.delete(data_id))
        #
        #
        #     # Test the group GET function
        #     # It should get a set of events which are then
        #     # placed into a list.  Elements of the list should
        #     # be of type Event.
        #     event_list_from_group = list(ObaseApi.Event.get())
        #     self.assertIsInstance(event_list_from_group, list)
        #     self.assertIsInstance(event_list_from_group[0], Event)
        #
        # def test_Message(self):
        #
        #     # Create initial test data for testing POST
        #     test_time = datetime.now()
        #     test_data = {
        #         'created': test_time,
        #         'updated': test_time,
        #         'data_blob': ["{'cool': 'pants', 'hammer': 'time'}"]
        #     }
        #
        #     # POST the data and save the ID
        #     posted_data = ObaseApi.Data.post(test_data)
        #     data_id = posted_data.id
        #
        #     # Create initial test Event field data
        #     test_event_fields = {
        #         'created': test_time,
        #         'updated': test_time,
        #         'datetime': test_time,
        #         'user_id': 1138,
        #         'provider_id': 10591,
        #         'signal_id': 1812,
        #         'provider_name': 'TwitFace',
        #         'data': data_id,
        #         # 'location':
        #     }
        #
        #     # POST the Event and save the ID
        #     posted_event_from_db = ObaseApi.Event.post(test_event_fields)
        #     event_id = posted_event_from_db.id
        #
        #     test_message_fields = {
        #         'message_to': ['John Cook'],
        #         'message_from': 'Mike Adams',
        #         'message_body': 'You are a stupid head.',
        #         'event': event_id
        #     }
        #
        #     # POST the Message, save the ID, then GET the Message back and check
        #     # that some fields are correct, which indicates the POST was successful
        #     posted_message_from_db = ObaseApi.Message.post(test_message_fields)
        #     message_id = posted_message_from_db.id
        #
        #     get_message_from_db = ObaseApi.Message.get(message_id)
        #     self.assertEqual(get_message_from_db['message_to'], ['John Cook'])
        #     self.assertEqual(get_message_from_db['message_body'], 'You are a stupid head.')
        #     self.assertEqual(ObaseApi.Event.get(get_message_from_db.event.id)['provider_name'], 'TwitFace')
        #     self.assertEqual(posted_message_from_db, get_message_from_db)
        #
        #
        #     # Create new Message field data for the PUT test
        #     test_message_fields['message_to'] = ['Jimmy Garoppolo']
        #     test_message_fields['message_body'] = 'Actually, you are a stupid face.'
        #
        #     # Test Message PUT by running it and checking that the new field data is returned,
        #     # Event should be the same since it isn't changed
        #     put_message_from_db = ObaseApi.Message.put(message_id, test_message_fields)
        #     self.assertEqual(put_message_from_db['message_to'], ['Jimmy Garoppolo'])
        #     self.assertEqual(put_message_from_db['message_from'], 'Mike Adams')
        #     self.assertEqual(ObaseApi.Event.get(put_message_from_db.event.id)['provider_name'], 'TwitFace')
        #     self.assertEqual(put_message_from_db, get_message_from_db)
        #
        #     # Create new Event field data for the PATCH test
        #     test_message_fields['message_from'] = 'Marvin the Martian'
        #
        #     # Test Message PATCH by running it and checking that the new field data is returned,
        #     # Also check that some old data hasn't changed
        #     patch_message_from_db = ObaseApi.Message.patch(message_id, {'message_from': test_message_fields['message_from']})
        #     self.assertEqual(patch_message_from_db['message_from'], test_message_fields['message_from'])
        #     self.assertEqual(patch_message_from_db['message_to'], test_message_fields['message_to'])
        #     self.assertEqual(ObaseApi.Event.get(get_message_from_db.event.id)['provider_name'], test_event_fields['provider_name'])
        #     self.assertEqual(patch_message_from_db, get_message_from_db)
        #
        #     # DELETE the Message and check that the response is True,
        #     # which means the request was successful
        #     self.assertTrue(ObaseApi.Message.delete(message_id))
        #     self.assertTrue(ObaseApi.Event.delete(event_id))
        #     self.assertTrue(ObaseApi.Data.delete(data_id))
        #
        #
        #     # Test the group GET function
        #     # It should get a set of events which are then
        #     # placed into a list.  Elements of the list should
        #     # be of type Event.
        #     message_list_from_group = list(ObaseApi.Message.get())
        #     self.assertIsInstance(message_list_from_group, list)
        #     self.assertIsInstance(message_list_from_group[0], Message)
