from __future__ import unicode_literals

from django.contrib import admin

from ografy.apps.keyauth.models import Key, Address


class KeyAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Key, KeyAdmin)
admin.site.register(Address, AddressAdmin)
