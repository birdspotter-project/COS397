from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    if request.method == "POST":
        form = ImportShapefileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            date_created = form.cleaned_data['created_date']
            import_shapefile(request, form.cleaned_data['file_to_import'], form.cleaned_data['created_date'])
            return render(request, 'success.html', {'redirect': '/'})
    form = ImportShapefileForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'upload.html', context)
