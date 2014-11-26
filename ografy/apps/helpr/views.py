from django.shortcuts import render


def index(request):
    return render(request, 'helpr/index.html', {
        'title': 'Ografy - Documentation'
    })
