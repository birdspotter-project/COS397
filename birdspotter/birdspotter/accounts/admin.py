from django.contrib import admin
from birdspotter.accounts.models import User

class UserAdmin(admin.ModelAdmin):
	pass
admin.site.register(User, UserAdmin)
