from django.shortcuts import render

from ografy.contrib.multiauth.decorators import login_required


@login_required
def main(request):
    return render(request, 'explorer/main.html', {
        'title': 'Explore'
    })
