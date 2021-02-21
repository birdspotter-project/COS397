from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import QueueJobForm
from .scripts.start_job import start_job

@login_required
def index(request):
    """Landing page for analysis path
    """
    args = {}

    if request.method == "POST":
        form = QueueJobForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success = start_job(request, form.cleaned_data['file_to_import'], form.cleaned_data['created_date'])
            if success:
                args['statusDiv'] = "File upload successful"
                args['result'] = "success"
                args['redirect'] = "/"
            else:
                args['statusDiv'] = "Job Queue Failed, please contact your administrator"
                args['result'] = "danger"
                args['redirect'] = "/anaylis/"
            return render(request, 'result.html', args)
    form = QueueJobForm()
    context = {
        'form': form,
        'isAdmin': False
    }
    return render(request, 'analyze.html', context)