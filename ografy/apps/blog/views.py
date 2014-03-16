from __future__ import unicode_literals

from django.shortcuts import render


def index(request):
    return render(request, 'blog/index.html', {
        'title': 'Ografy - Development Blog'
    })
