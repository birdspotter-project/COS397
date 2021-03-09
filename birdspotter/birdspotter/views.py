from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
from birdspotter.accounts.models import User
from birdspotter.dataio.models import Dataset
from .forms import DatasetEditForm
from django.contrib import messages
from django.http import HttpResponse


def index(request):
    """
    Application index which is also the landing page. This view displays a table with all datasets available to the
    currently authenticated user, otherwise, display only public facing datasets.
    """
    if request.user.is_authenticated:
        datasets = get_datasets_for_user(request.user).values()
    else:
        datasets = get_public_datasets().values()
    return render(request, 'index.html', {'datasets': datasets})


@login_required
def edit_dataset(request, uuid):
    """
    Editing dataset metadata, such as dataset name, comments, and whether the dataset is public
    """
    user = request.user
    dataset = Dataset.objects.filter(owner_id=user.id).get(dataset_id=uuid)
    if dataset is not None:
        form = DatasetEditForm(request.POST or None, instance=dataset)
        if form.is_valid():
            form.save()
            messages.success(request, "Data set edit complete")
            return redirect("/")
    form = DatasetEditForm(initial={
    'name': dataset.name,
    'is_public': dataset.is_public,
    })
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, "dataset_edit.html", context=context)


# How to correctly send a fully compliant HTTP 204 response, based on https://code.djangoproject.com/ticket/16632
class HttpResponseNoContent(HttpResponse):
    """Special HTTP response with no content, just headers.

    The content operations are ignored.
    """

    def __init__(self, content="", mimetype=None, status=None, content_type=None): # noqa
        super().__init__(status=204)

        if "content-type" in self._headers:
            del self._headers["content-type"]

    def _set_content(self, value):
        pass

    def _get_content(self, value):
        pass


def auth(request):
    """
    Used by NGINX to check if the user is authorized with minimal overhead.
    """
    if request.user.is_authenticated:
        return HttpResponseNoContent()
    return HttpResponse(status=403)
