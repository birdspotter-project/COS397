from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.response import TemplateResponse

from .forms import ImportShapefileForm
from .scripts.import_handler import import_shapefile

@login_required
def index(request):
    """Landing page for dataio path

    Args:
        request (HTTPRequest): Description

    Returns:
        render
    """
    args = {}

    if request.method == "POST":
        form = ImportShapefileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            date_created = form.cleaned_data['created_date']
            success = import_shapefile(request, form.cleaned_data['file_to_import'], form.cleaned_data['created_date'])
            if success:
                args['statusDiv'] = "File upload successful"
                return TemplateResponse(request, 'success.html', args)
                #return render(request, 'template.html', {'redirect': '/'})
            else:
                args['statusDiv'] = "File upload fail, please upload a valid zipfile"
                return TemplateResponse(request, 'success.html', args)
                #return render(request, 'template.html', {'redirect': '/'})

    form = ImportShapefileForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'upload.html', context)
