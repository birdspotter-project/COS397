from django.contrib import admin
from birdspotter.dataio.models import Dataset

class DatasetAdmin(admin.ModelAdmin):
	pass
admin.site.register(Dataset, DatasetAdmin)
