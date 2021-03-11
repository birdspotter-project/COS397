from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
import logging
from django.conf import settings
from .forms import ImportForm, ShareDatasetForm
from .scripts.import_handler import import_data
from .models import Dataset
from django.shortcuts import redirect

from django.core.serializers import serialize

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
            success = import_data(request.user, form.cleaned_data['file_path'], form.cleaned_data['file_name'], form.cleaned_data['created_date'], form.cleaned_data['public'])
            if success:
                messages.success(request, "File processing successful")
            else:
                messages.error(request, "File processing failed, please upload a valid zipfile or GeoTiff")
            return redirect('/')
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


def share_dataset(request, dataset_id):
    if request.method == "POST":
        dataset = Dataset.objects.get(dataset_id=dataset_id)
        form = ShareDatasetForm(request.POST, instance=dataset)
        if form.is_valid():
            form.save()
            messages.success(request, "Dataset shared with users")
            return redirect('/')

    dataset = Dataset.objects.get(dataset_id=dataset_id)
    form = ShareDatasetForm(instance=dataset)
    return render(request, 'share.html', {'form': form})

def share_test(request, dataset_id):
    dataset = Dataset.objects.get(dataset_id=dataset_id)
    if request.method == "POST":
        """
        Get all checked values and add the users to dataset.shared_with
        """
        print("here")
        user_ids = [request.POST.get('users[]')]
        User = get_user_model()
        users = User.objects.filter(user_id__in=user_ids)
        print(users)
        dataset.shared_with.add(*users)
        print(dataset.shared_with.all())

        return HttpResponse(status=200)

    elif request.method == "GET":
        """
        Return with list of all users and if the dataset is shared with them
        """
        User = get_user_model()
        data = []
        for u in User.objects.all():
            if not u == request.user:
                data.append({"user_id": u.user_id, "username": u.username, "is_shared": u in dataset.shared_with.all()})
        return JsonResponse({"users": data}, safe=False)