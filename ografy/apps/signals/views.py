from __future__ import unicode_literals
import copy
import json

from django.conf import settings
from django.http import HttpResponse


def index(request):
    config = copy.deepcopy(settings.SIGNALS)

    return HttpResponse(json.dumps(config), content_type='application/json')
