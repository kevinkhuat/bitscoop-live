from __future__ import unicode_literals

from django.contrib import admin

from ografy.apps.xauth.models import User, Key, Address


class UserAdmin(admin.ModelAdmin):
    exclude = ('upper_email', 'upper_handle',)


class KeyAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Address, AddressAdmin)
