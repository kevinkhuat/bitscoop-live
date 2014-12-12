from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def my_profile(request):
    return render(request, 'core/user/my_profile.html', {
        'title': 'Ografy - {0}'.format(request.user.identifier),
        'user': request.user
    })


def profile(request, handle):
    User = get_user_model()

    user = User.objects.filter(handle__iexact=handle).first()

    if user is None:
        raise Http404

    template = 'core/user/profile.html'
    # if user == request.user:
    #     template = 'user/my_profile.html'
    # else:
    #     template = 'user/profile.html'

    return render(request, template, {
        'title': 'Ografy - {0}'.format(user.handle),
        'user': user
    })


# Ografy Account specific login/logout
def providers(request):
    return render(request, 'core/user/providers.html', {
        # 'title': 'Ografy - {0}'.format(request.user.identifier),
        # 'user': request.user
    })

def signals(request, pk):
    return render(request, 'core/user/signals.html', {
        # 'title': 'Ografy - {0}'.format(request.user.identifier),
        # 'user': request.user
    })