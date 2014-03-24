from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ografy.lib.xauth.decorators import key_login


@key_login
def index(request):
    return redirect(reverse('demo_info'))


@login_required
def info(request):
    return render(request, 'demo/info.html', {
        'title': 'Ografy - Info'
    })


@login_required
def plan(request):
    return render(request, 'demo/plan.html', {
        'title': 'Ografy - Plan'
    })


@login_required
def dashboard(request):
    return render(request, 'demo/dashboard.html', {
        'title': 'Ografy - Dashboard'
    })
