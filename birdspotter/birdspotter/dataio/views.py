from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImportForm
import logging
from django.conf import settings
from .forms import ImportForm
from .scripts.import_handler import import_data
from django.shortcuts import redirect
@login_required
def index(request):
    """Landing page for dataio path

    Args:
        request (HTTPRequest): api requst

    Returns:
        Attempts to import the uploaded shapefile and notifies the user if the import was sucessful
    """
    if request.method == "POST":
        form = ImportForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "File uploaded, starting processing")
            success = import_data(request.user, form.cleaned_data['file_path'], form.cleaned_data['file_name'], form.cleaned_data['created_date'])
            if success:
                messages.success(request, "File processing successful")
                return redirect("/")
            else:
                messages.error(request, "File processing failed, please upload a valid zipfile or GeoTiff")
                return redirect("/import/")
        if (settings.DEBUG.lower == "true" or request.user.is_admin()):
            messages.error(request, f"Errors: {form.errors}", extra_tags='safe')
        else:
            messages.error(request, "File upload failed, please contact your administrator.")
        logging.error(form.errors)
        logging.error(dict(form.data))
        form = ImportForm()
        context = {
            'form': form,
            'isAdmin': False
        }
        return render(request, 'upload.html', context, status=400)
    form = ImportForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'upload.html', context)
