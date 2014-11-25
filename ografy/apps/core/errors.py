from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def view400(request):
    template = 'core/400.html'
    context = {
        'title': 'Ografy - 400 (Bad Request)'
    }

    return render(request, template, context)


def view403(request):
    template = 'core/403.html'
    context = {
        'title': 'Ografy - 403 (Forbidden)'
    }

    return render(request, template, context)


def view404(request):
    template = 'core/404.html'
    context = {
        'title': 'Ografy - 404 (Page Not Found)'
    }

    return render(request, template, context)


def view500(request):
    template = 'core/500.html'
    context = {
        'title': 'Ografy - 500 (Server Runtime Error)'
    }

    return render(request, template, context)
