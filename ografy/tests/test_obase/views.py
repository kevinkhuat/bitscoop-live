import jsonpickle

from django.shortcuts import render
from ografy.apps.obase.documents import Event


# @login_required
def form(request):
    return render(request, 'form.html')

# @login_required
def obase_list(request):
    event_list = []

    for event in Event.get_all():
        #FIXME: Use a custom serializer
        event['_id'] = int.from_bytes(event['_id']._ObjectId__id, 'big')
        event_list.append(jsonpickle.encode(event))

    return render(request, 'list.html', {
        'event_list': event_list
    })
