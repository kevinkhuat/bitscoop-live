from __future__ import unicode_literals

from tastypie import fields
from tastydata.resources import Resource

from ografy.apps.core.models import Account, Entry, User


class UserResource(Resource):
    class Meta:
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