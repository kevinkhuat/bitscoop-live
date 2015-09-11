from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render

from ografy.contrib.multiauth.decorators import login_required


@login_required
def my_profile(request):
    return render(request, 'core/user/my_profile.html', {
        'title': 'Ografy - {0}'.format(request.user.identifier),
        'lockwidth_override': True,
        'selected': 'user',
        'user': request.user
    })


@login_required
def profile(request, handle):
    user_model = get_user_model()

    user = user_model.objects.filter(handle__iexact=handle).first()

    if user is None:
        raise Http404

    template = 'core/user/profile.html'
    # if user == request.user:
    #     template = 'user/my_profile.html'
    # else:
    #     template = 'user/profile.html'

    return render(request, template, {
        'title': 'Ografy - {0}'.format(user.handle),
        'lockwidth_override': True,
        'user': user
    })


@login_required
def signals(request, pk):
    return render(request, 'core/user/signals.html', {
        # 'title': 'Ografy - {0}'.format(request.user.identifier),
        # 'user': request.user
    })
