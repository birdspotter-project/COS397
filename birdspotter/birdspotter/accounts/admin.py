from django.contrib.auth.admin import UserAdmin as usradmin
from django.contrib import admin
from birdspotter.accounts.models import User

class UserAdmin(usradmin):
	pass
admin.site.register(User, UserAdmin)
