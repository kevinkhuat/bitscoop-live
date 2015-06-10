from django.shortcuts import render


def index(request):
    return render(request, 'new/index.html', {
        'title': 'Testbed'
    })
