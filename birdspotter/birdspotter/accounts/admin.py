from django.contrib import admin as admin
from django.contrib.auth.admin import UserAdmin

from birdspotter.accounts.models import User, GroupRequest


class UserModelAdmin(UserAdmin):
    pass


admin.site.register(User, UserModelAdmin)


class GroupRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupRequest, GroupRequestAdmin)
