from django.contrib import admin
from birdspotter.analysis.models import Algorithm


# Registering algorithm so that admins can add algorithms
admin.site.register(Algorithm)
