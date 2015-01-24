from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from ografy.apps.obase import api as obase_api
from ografy.apps.obase.documents import Event


@login_required()
def main(request):
    template = 'core/main/main.html'

    return render(request, template, {
        'user': request.user
    })

#
# @login_required()
# def list_view(request):
#     template = 'core/main/base.html'
#
#     events = list(Event.objects(user_id=request.user.id))
#
#     return render(request, template, {
#         'title': 'Ografy - {0}'.format(request.user.identifier),
#         'body_class': 'full',
#         'user': request.user,
#         'events': events,
#         'list': True
#     })
#
#
# @login_required()
# def map(request):
#     template = 'core/main/map.html'
#
#     events = list(Event.objects(user_id=request.user.id))
#
#     return render(request, template, {
#         'title': 'Ografy - {0}'.format(request.user.identifier),
#         'body_class': 'full',
#         'user': request.user,
#         'events': events
#     })
#
#
# @login_required()
# def timeline(request):
#     template = 'core/main/map.html'
#
#     events = list(Event.objects(user_id=request.user.id))
#
#     return render(request, template, {
#         'title': 'Ografy - {0}'.format(request.user.identifier),
#         'body_class': 'full',
#         'user': request.user,
#         'events': events
#     })