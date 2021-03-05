from django.shortcuts import render, redirect
from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
from birdspotter.accounts.models import User
from birdspotter.dataio.models import Dataset
from .forms import DatasetEditForm
from django.contrib import messages


def index(request):
    """
    Application index which is also the landing page. This view displays a table with all datasets available to the
    currently authenticated user, otherwise, display only public facing datasets.
    """
    current_user = None
    try:
        current_user = User.objects.get_by_natural_key(request.user)
    except Exception:
        print('Could not find user: %s' % request.user.username)
    if current_user:
        datasets = get_datasets_for_user(current_user).values()
    else:
        datasets = None
    return render(request, 'index.html', {'datasets': datasets})

@login_required
def edit_dataset(request, uuid):
    """
    Editing dataset metadata.
    """
    user = request.user
    dataset = Dataset.objects.filter(owner_id=user.id).get(dataset_id=uuid)
    if dataset is not None:
        form = DatasetEditForm(request.POST or None, instance=dataset)
        if form.is_valid():
            form.save()
            return redirect("/")
        messages.error(request, "Failed to edit dataset metadata")
    form = DatasetEditForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, "dataset_edit.html", context=context)