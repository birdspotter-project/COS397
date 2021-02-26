from django.contrib.auth.admin import UserAdmin as usradmin
from django.contrib import admin as admin

from birdspotter.accounts.models import User, GroupRequest

class UserAdmin(usradmin):
	pass


admin.site.register(User, UserAdmin)

class GroupRequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(GroupRequest, GroupRequestAdmin)