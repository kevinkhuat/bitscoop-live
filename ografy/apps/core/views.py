from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View


def index(request):
    return render(request, 'core/home/index.html', {
        'title': 'Ografy'
    })



class LoginView(View):
    def get(self, request):
        return render(request, 'core/user/login.html', {
            'title': 'Ografy - Login'
        })

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(args)
        print(kwargs)

        return render(request, 'core/user/login.html', {
            'title': 'Ografy - Loggged in!'
        })
