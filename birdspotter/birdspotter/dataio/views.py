from django.shortcuts import render
from django.http import HttpResponse
from .scripts.import_handler import import_shapefile
from datetime import datetime, date
from .forms import ImportShapefileForm


def index(request):
	if request.method == "POST":
		form = ImportShapefileForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			date_created = form.cleaned_data['created_date']
			import_shapefile(form.cleaned_data['file_to_import'], form.cleaned_data['created_date'])
			return render(request, 'success.html', {'redirect': '/'})
	else:
		form = ImportShapefileForm()
	context = {
		'form': form,
		'isAdmin': False
	}
	return render(request, 'upload.html', context)