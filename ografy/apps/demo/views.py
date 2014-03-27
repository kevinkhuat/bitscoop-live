from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ografy.lib.xauth.decorators import key_login, membership_required


@key_login
def login(request):
    return redirect(reverse('demo_info'))


@membership_required('Investors')
@login_required
def info(request):
    return render(request, 'demo/info.html', {
        'title': 'Ografy - Info'
    })


@membership_required('Investors')
@login_required
def plan(request):
    return render(request, 'demo/plan.html', {
        'title': 'Ografy - Plan'
    })


@membership_required('Investors')
@login_required
def examples(request):
    return render(request, 'demo/examples.html', {
        'title': 'Ografy - Examples'
    })


@membership_required('Investors')
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {
        'title': 'Ografy - Dashboard'
    })


@membership_required('Investors')
@login_required
def infographic(request):
    return render(request, 'demo/infographic.html')
