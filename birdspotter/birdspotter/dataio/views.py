from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.conf import settings
import logging
import os

from .forms import ImportForm
from .scripts.import_handler import import_new_data
from .models import Dataset, RawData, RawShapefile
from birdspotter.utils import GROUPS
from private_storage.views import PrivateStorageDetailView

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
            success = import_new_data(request.user, form.cleaned_data['file_path'],
                                  form.cleaned_data['public'], form.cleaned_data['file_name'])
            if success:
                messages.success(request, "File processing successful")
                return redirect("/")
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

@login_required
def share_dataset(request, dataset_id):
    """
    Handles the share dialog and accepts GET and POST requests to /share/<dataset_id>/
    POST: Get list of user_ids and add users to dataset.shared_with
    GET: Returns an object with an array of usernames, along with if they are already shared the dataset
    """
    dataset = Dataset.objects.get(dataset_id=dataset_id)
    # only allow owner of dataset to share the dataset
    if dataset.owner == request.user:
        User = get_user_model()
        if request.method == "POST":
            # and array of users is specified with the [] appended to the json key
            add_shared = request.POST.getlist('add_share[]')
            remove_shared = request.POST.getlist('remove_share[]')

            # add users to share
            users = User.objects.filter(user_id__in=add_shared).all()
            dataset.shared_with.add(*users)

            # remove users from share
            users = User.objects.filter(user_id__in=remove_shared).all()
            dataset.shared_with.remove(*users)

            dataset.save()
            messages.success(request, "Dataset successfully shared with users")
            return HttpResponse(status=200, content='Dataset sharing successfully updated')
        if request.method == "GET":
            data = []
            for u in User.objects.all():
                if not u == request.user:
                    data.append({"user_id": u.user_id, "username": u.username, "is_shared": u in dataset.shared_with.all()})
            return JsonResponse({"users": data}, safe=False)
        return HttpResponse(status=405)
    raise PermissionDenied


@login_required
def export_dataset(request, dataset_id):
    """
    Handles the export dialog and accepts GET and POST requests to /export/<dataset_id>/
    POST: Get list of potential raw_data's
    GET: Returns an object with an array of usernames, along with if they are already shared the dataset
    """
    dataset = Dataset.objects.get(dataset_id=dataset_id)
    # only allow owner of dataset to share the dataset
    if dataset.owner == request.user or request.user.is_admin() or request.user.groups.filter(name=GROUPS.privileged).exists():
        if request.method == "GET":
            data_id = ""
            if dataset.geotiff:
                data_id = dataset.geotiff.pk
                # the name is synced here because this is the only time it matters that it's synced
                dataset.geotiff.name = dataset.name
                dataset.geotiff.save()
            elif RawShapefile.objects.filter(dataset=dataset).exists():
                rawshp = RawShapefile.objects.filter(dataset=dataset)[0].rawshp
                data_id = rawshp.pk
                # the name is synced here because this is the only time it matters that it's synced
                rawshp.name = dataset.name
                rawshp.save()
            else:
                messages.error(request, "No data stored for this dataset")
                return redirect("/")
            messages.success(request, "Dataset Downloaded")
            return redirect(f"/rawdata/{data_id}")
    raise PermissionDenied


class raw_data(PrivateStorageDetailView):
    model = RawData
    model_file_field = 'path'
    model_file_name = 'name'
    model_file_ext = 'ext'
    content_disposition = 'inline'
    def get_content_disposition_filename(self, private_file):
        name = getattr(self.object, self.model_file_name)
        ext = getattr(self.object, self.model_file_ext)
        return f"{name}.{ext}" or os.path.basename(private_file.relative_name)
