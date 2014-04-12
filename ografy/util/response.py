from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def redirect_by_name(url_name):
    return redirect(reverse(url_name))

