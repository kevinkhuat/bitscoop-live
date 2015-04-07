import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.views.generic import View

from ografy.settings import OGRAFY_MAPBOX_ACCESS_TOKEN

@login_required()
def main(request):
	template = 'core/main/main.html'

	return render(request, template, {
		'user': request.user
	})

# @login_required()
# class mapbox_token(View):
#
# 	def get(self, request):
# 		data = {'OGRAFY_MAPBOX_ACCESS_TOKEN': OGRAFY_MAPBOX_ACCESS_TOKEN}
# 		return HttpResponse(json.dumps(data), content_type='application/json')

@login_required()
def mapbox_token(request):
		data = {'OGRAFY_MAPBOX_ACCESS_TOKEN': OGRAFY_MAPBOX_ACCESS_TOKEN}
		return HttpResponse(json.dumps(data), content_type='application/json')