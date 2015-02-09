import ografy.apps.obase.api as ObaseAPI
from ografy.apps.obase.documents import Data, Event
from django.core.management.base import BaseCommand, CommandError
from bson.objectid import ObjectId

import datetime

class Command(BaseCommand):

	def handle(self, *args, **options):
			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 12, 1, 19, 54, 6),
				updated = datetime.datetime(2014, 12, 1, 19, 54, 6),
				signal_id = 2,
				provider_id = 3,
				provider_name = 'steam',
				datetime = datetime.datetime(2014, 12, 1, 19, 54, 6),
				data = ObjectId("54d110db4b757538b165763a"),
				name = 'Thomas',
				location = [ -73.68, 40.68832 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2013, 2, 1, 11, 23, 6),
				updated = datetime.datetime(2013, 4, 1, 13, 2, 6),
				signal_id = 2,
				provider_id = 3,
				provider_name = 'steam',
				datetime = datetime.datetime(2013, 4, 1, 13, 2, 6),
				data = ObjectId("54d110db4b757538b165763b"),
				name = 'Sam',
				location = [ -73.687, 40.68830 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 2,
				created = datetime.datetime(2014, 12, 1, 19, 54, 6),
				updated = datetime.datetime(2014, 12, 1, 19, 54, 6),
				signal_id = 1,
				provider_id = 1,
				provider_name = 'facebook',
				datetime = datetime.datetime(2014, 12, 1, 19, 54, 6),
				data = ObjectId("54d110db4b757538b165763c"),
				name = 'Sam',
				location = [ -73.68, 40.68717 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 12, 3, 19, 54, 6),
				updated = datetime.datetime(2014, 12, 3, 19, 54, 6),
				signal_id = 1,
				provider_id = 1,
				provider_name = 'facebook',
				datetime = datetime.datetime(2014, 12, 3, 19, 54, 6),
				data = ObjectId("54d110db4b757538b165763d"),
				name = 'John',
				location = [ -73.68, 40.68888 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 12, 8, 19, 54, 6),
				updated = datetime.datetime(2014, 12, 8, 19, 54, 6),
				signal_id = 3,
				provider_id = 8,
				provider_name = 'github',
				datetime = datetime.datetime(2014, 12, 8, 19, 54, 6),
				data = ObjectId("54d110db4b757538b165763e"),
				name = 'Sam',
				location = [ -73.683, 40.68844 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 11, 3, 19, 54, 6),
				updated = datetime.datetime(2014, 11, 3, 19, 54, 6),
				signal_id = 1,
				provider_id = 1,
				provider_name = 'facebook',
				datetime = datetime.datetime(2014, 11, 3, 19, 54, 6),
				data = ObjectId("54d110db4b757538b165763f"),
				name = 'John',
				location = [ -73.68, 40.68852 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 3, 2, 19, 54, 6),
				updated = datetime.datetime(2014, 3, 2, 19, 54, 6),
				signal_id = 4,
				provider_id = 2,
				provider_name = 'twitter',
				datetime = datetime.datetime(2014, 3, 2, 19, 54, 6),
				data = ObjectId("54d110db4b757538b1657640"),
				name = 'Samantha',
				location = [ -73.682, 40.68890 ]
			)

			ObaseAPI.EventApi.post(test_data)

			test_data = Event(
				user_id = 1,
				created = datetime.datetime(2014, 12, 14, 19, 54, 6),
				updated = datetime.datetime(2014, 12, 14, 19, 54, 6),
				signal_id = 2,
				provider_id = 3,
				provider_name = 'steam',
				datetime = datetime.datetime(2014, 12, 14, 19, 54, 6),
				data = ObjectId("54d110db4b757538b1657641"),
				name = 'John',
				location = [ -93.67, 40.68831 ]
			)

			ObaseAPI.EventApi.post(test_data)