from django.contrib import admin
from birdspotter.analysis.models import Algorithm, AnalysisJob

admin.site.register(Algorithm)
admin.site.register(AnalysisJob)
# Register your models here.
