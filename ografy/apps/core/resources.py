from __future__ import unicode_literals

from tastypie import fields
from tastydata.resources import Resource

from ografy.apps.core.models import Entry, User


class UserResource(Resource):
    #entries = fields.ToManyField('ografy.apps.core.resources.EntryResource', 'entry_set', related_name='entries')

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']


#class EntryResource(Resource):
#    user = fields.ForeignKey(UserResource, 'user')
#
#    class Meta:
#        queryset = Entry.objects.all()
#        allowed_methods = ['get']