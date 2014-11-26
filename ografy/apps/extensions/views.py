from django.shortcuts import render


def index(request):
    return render(request, 'extensions/index.html', {
        'title': 'Ografy - Extensions'
    })
