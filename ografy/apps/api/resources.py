from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from tastypie import fields

from ografy.apps.core.models import Account, Entry
from ografy.lib.tastydata.resources import Resource


class UserResource(Resource):
    class Meta:
        User = get_user_model()
        queryset = User.objects.all()
        allowed_methods = ['get']


class AccountResource(Resource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Account.objects.all()
        allowed_methods = ['get']


class EntryResource(Resource):
    account = fields.ForeignKey(AccountResource, 'account')

    class Meta:
        queryset = Entry.objects.all()
        allowed_methods = ['get']
