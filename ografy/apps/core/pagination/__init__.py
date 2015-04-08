from rest_framework.pagination import PageNumberPagination, Response

class TwentyItemPagination(PageNumberPagination):
	def get_paginated_response(self, data):
		return Response({
			'links': {
				'next': self.get_next_link(),
				'previous': self.get_previous_link()
			},
			'count': self.page.paginator.count,
			'results': data
		})
	page_size = 20
	page_size_query_param = 'page_size'
	max_page_size = 20