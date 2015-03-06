from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def main(request):
    template = 'core/main/main.html'

    return render(request, template, {
        'user': request.user
    })
