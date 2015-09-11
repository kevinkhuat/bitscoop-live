import json

from django.shortcuts import HttpResponse, render

from ografy.contrib.multiauth.decorators import login_required
from ografy.settings import OGRAFY_MAPBOX_ACCESS_TOKEN


@login_required
def main(request):
    template = 'core/main/main.html'

    return render(request, template, {
        'user': request.user
    })


@login_required
def mapbox_token(request):
    data = {
        'OGRAFY_MAPBOX_ACCESS_TOKEN': OGRAFY_MAPBOX_ACCESS_TOKEN
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
