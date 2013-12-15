from __future__ import unicode_literals

from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html', {
        'title': 'Ografy'
    })


def blog(request):
    return render(request, 'core/blog/index.html', {
        'title': 'Ografy - Development Blog'
    })


def documentation(request):
    return render(request, 'core/documentation/index.html', {
        'title': 'Ografy - Documentation'
    })