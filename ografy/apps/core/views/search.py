import re

from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q

from ografy.apps.opi.views import DataView as dataView
from ografy.apps.opi.views import EventView as eventView
from  ografy.apps.opi.views import MessageView as messageView

class SearchView(View):
	def tokenize(val):

		expr = re.compile('\w+|"[^"]+"')
		tokens = expr.findall(val)

		for i in range(len(tokens)):
			tokens[i] = tokens[i].replace('"', '')

		return tokens

	def post(self, request):
		#Any letter (one or more) OR Quote, anything not a quote (one or more), quote

		deserialized = request.body.decode('utf-8')
		deserialized_split = deserialized.split('&')

		search_terms_json = deserialized_split[0]
		search_terms_data = search_terms_json.split('=')[1]
		search_terms_replaced_characters = search_terms_data.replace('%22', '"').replace('+', ' ')

		filter_string_json = deserialized_split[1]
		filter_string_data = filter_string_json.split('=')[1]
		filter_string_replaced_characters = filter_string_data.replace('+', ' ').replace('%2F', '/').replace('%3A', ':')

		tokens = SearchView.tokenize(search_terms_replaced_characters)


		dataView.get(Q(filter_string_replaced_characters))
		return_dict = {}
		for i in range(len(tokens)):
			return_dict[i] = tokens[i]

		# get_query = obase_api.EventApi.get(
		# 			request.auth_filter &
		# 			MongoAPIView.Meta.Q(tokens)
		# 		)

		return JsonResponse(return_dict)
