from django.shortcuts import render

from server.contrib.multiauth.decorators import login_required


@login_required
def main(request, search_id):
    return render(request, 'explorer/main.html', {
        'title': 'Explore'
    })
