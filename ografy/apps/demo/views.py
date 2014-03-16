from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ografy.lib.auth.decorators import key_login


@key_login
def index(request):
    return render(request, 'demo/index.html', {
        'title': 'Ografy - Demo'
    })


#@login_required
def debug(request):
    return render(request, 'demo/index.html', {
        'title': 'Ografy - Debug'
    })
