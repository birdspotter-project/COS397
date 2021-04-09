from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from birdspotter.accounts.models import User, GroupRequest



class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups',)}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserModelAdmin)
admin.site.register(GroupRequest)
