from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ografy.apps.keyauth.decorators import key_login


def index(request):
    return render(request, 'core/home/index.html', {
        'title': 'Ografy'
    })


@key_login
def demo(request):
    print(request.user)

    return render(request, 'core/demo/index.html', {
        'title': 'Ografy - Demo'
    })


def dashboard(request):
    return render(request, 'core/dashboard/index.html', {
        'title': 'Ografy - Dashboard'
    })


def blog(request):
    return render(request, 'core/blog/index.html', {
        'title': 'Ografy - Development Blog'
    })


def documentation(request):
    return render(request, 'core/documentation/index.html', {
        'title': 'Ografy - Documentation'
    })


def debug(request):
    print(request.session.session_key)
    print(request.user)

    return render(request, 'core/demo/index.html', {
        'title': 'Ografy - Debug'
    })
