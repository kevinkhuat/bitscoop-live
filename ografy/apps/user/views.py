from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render


User = get_user_model()


def index(request):
    return render(request, 'user/index.html', {
        'title': 'Ografy - User'
    })


def profile(request, oid):
    user = User.objects.by_oid(oid).first()

    if user is None:
        raise Http404

    if user == request.user:
        template = 'user/my_profile.html'
    else:
        template = 'user/profile.html'

    return render(request, template, {
        'title': 'Ografy - ' + user.identifier,
        'user': user
    })
