from django.shortcuts import render
from ografy.apps.obase.api import Event


# @login_required
def form(request):
    return render(request, 'form.html')


# @login_required
def obase_list(request):
    EventList = Event.get()
    event_list = []

    for event in EventList:
        #FIXME: Use a custom serializer
        # event['id'] = int.from_bytes(event['id']._ObjectId__id, 'big')
        event_list.append(event['id'])

    return render(request, 'list.html', {
        'event_list': event_list
    })
