from django.shortcuts import render


def index(request):
    return render(request, 'documentation/index.html', {
        'title': 'Ografy - Documentation'
    })
