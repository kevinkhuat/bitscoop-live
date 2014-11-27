import json
from django.shortcuts import render
from ografy.apps.obase.documents import Event


# @login_required
def form(request):
    return render(request, 'form.html')


# @login_required
def obase_list(request):
    event_list = []

    for event in Event.objects:
        #FIXME: Use a custom serializer
        # event['id'] = int.from_bytes(event['id']._ObjectId__id, 'big')
        event_list.append(int.from_bytes(event['id']._ObjectId__id, 'big'))

    return render(request, 'list.html', {
        'event_list': event_list
    })
