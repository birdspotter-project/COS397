from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QueueJobForm
from .scripts.start_job import start_job
from .models import AnalysisJob

from birdspotter.utils import group_required, GROUPS


@login_required
def index(request):
    """User queue view to show active analysis jobs
    """
    jobs = AnalysisJob.objects.filter(owner=request.user.id).all()
    return render(request, "queue.html", {'jobs': jobs})


@login_required
@group_required(GROUPS.privileged, GROUPS.admin)
def queue_job(request, uuid):
    """Queuing form in order to queue datasets for external analysis
    """
    if request.method == "POST":
        form = QueueJobForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success = start_job(request, form.cleaned_data.get('algorithm'), uuid)
            if success:
                messages.success(request, "Job has been queued successfully")
                return redirect("/")
            messages.error(request, "Job Queue Failed, please contact your administrator")
            return redirect(f"/queue/{uuid}")
    form = QueueJobForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'analyze.html', context)