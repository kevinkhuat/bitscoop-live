from django.shortcuts import render


def index(request):
    if request.user.is_authenticated():
        template = 'core/user/home.html'
        context = {
            'title': 'Ografy - Home'
        }
    else:
        template = 'core/index.html'
        context = {
            'title': 'Ografy',
            'content_class': 'no-vertical-pad'
        }

    return render(request, template, context)


def contact(request):
    return render(request, 'core/contact.html', {
        'title': 'Ografy - Contact'
    })


def start(request):
    return render(request, 'core/start.html', {
        'title': 'Ografy - Get Started'
    })
