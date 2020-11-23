from django.shortcuts import render
from django.http import HttpResponse
from .scripts.import_handler import import_shapefile


def index(request):
	if request.method == "POST":
		if doc := request.FILES['document'] if 'document' in request.FILES else None:
			return HttpResponse(import_shapefile(doc))
	return render(request, 'upload.html', {'isAdmin': False})