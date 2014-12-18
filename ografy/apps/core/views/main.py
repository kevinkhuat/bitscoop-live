from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

@login_required()
def main(request):
    template = 'core/main.html'

    return render(request, template, {
        'title': 'Ografy - {0}'.format(request.user.identifier),
        'body_class': 'full',
        'user': request.user
    })