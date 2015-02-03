import ografy.apps.obase.api as ObaseAPI
from ografy.apps.obase.documents import Data
from django.core.management.base import BaseCommand, CommandError

import datetime

class Command(BaseCommand):

	def handle(self, *args, **options):
		for i in range(0, 8):
			test_data = Data(
				user_id = 1,
				created = datetime.datetime(2013, 12, 4, 19, 32, 4),
				updated = datetime.datetime(2014, 8, 4, 2, 8, 37),
				data_blob = ["{'cool': 'pants'}"]
			)
			ObaseAPI.DataApi.post(test_data)