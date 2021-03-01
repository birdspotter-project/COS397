from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import QueueJobForm
from .scripts.start_job import start_job
from .models import AnalysisJob
@login_required
def index(request):
    jobs = AnalysisJob.objects.filter(owner=request.user.id).all()
    return render(request, "queue.html", {'jobs': jobs})
@login_required
def queue_job(request, uuid):
    """Queuing form for external analysis
    """
    args = {}

    if request.method == "POST":
        form = QueueJobForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success = start_job(request, form.cleaned_data.get('algorithm'), uuid)
            if success:
                args['statusDiv'] = "File upload successful"
                args['result'] = "success"
                args['redirect'] = "/"
            else:
                args['statusDiv'] = "Job Queue Failed, please contact your administrator"
                args['result'] = "danger"
                args['redirect'] = request.path
            return render(request, 'result.html', args)
    form = QueueJobForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'analyze.html', context)