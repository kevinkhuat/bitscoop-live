import json

from django.conf import settings
from django.shortcuts import HttpResponse, render

from ografy.contrib.multiauth.decorators import login_required


@login_required
def main(request):
    template = 'core/main/main.html'

    return render(request, template, {
        'user': request.user
    })


@login_required
def mapbox_token(request):
    data = {
        'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
    }

    return HttpResponse(json.dumps(data), content_type='application/json')
