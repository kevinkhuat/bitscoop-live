from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


# @login_required
def form(request):
    return render(request, 'form.html')

# @login_required
def obase_list(request):
    return render(request, 'list.html')