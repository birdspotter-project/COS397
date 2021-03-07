from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImportShapefileForm
from .scripts.import_handler import import_data

@login_required
def index(request):
    """Landing page for dataio path

    Args:
        request (HTTPRequest): api requst

    Returns:
        Attempts to import the uploaded shapefile and notifies the user if the import was sucessful
    """
    if request.method == "POST":
        form = ImportShapefileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success = import_data(request.user, form.cleaned_data['file_to_import'], form.cleaned_data['created_date'])
            if success:
                messages.success(request, "File upload succeeded")
                return redirect("/")
            messages.error(request, "File upload succeeded, please try again or contact your administrator")
            return redirect("/import/")
    form = ImportShapefileForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'upload.html', context)
