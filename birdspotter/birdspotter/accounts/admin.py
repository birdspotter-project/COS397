from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from birdspotter.accounts.models import User, GroupRequest


class UserModelAdmin(UserAdmin):
    pass


admin.site.register(User, UserModelAdmin)
admin.site.register(GroupRequest)
