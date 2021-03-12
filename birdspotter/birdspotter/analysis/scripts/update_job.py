from birdspotter.analysis.models import AnalysisJob
import re
from django.conf import settings
from birdspotter.dataio.scripts.import_handler import import_data
import datetime
from birdspotter.dataio.models import Dataset


def handle_update(message):
    print(message.subject)
    update = parse_slurm(message.subject)
    job = AnalysisJob.objects.get(external_job_id=update['id'])
    job.status = update['status']
    job.save(update_fields='status')
    if job.status == "COMPLETED":
        import_results(job.external_job_id, job.owner)
        print("COMPLETED job " + job.external_job_id)
        
        
def parse_slurm(subj):
    raw = re.findall(r"Slurm Job_id=(\d*) Name=([\w\d]*) (\w*), Run time ([\d:]*), (\w*), ExitCode (\d*)", subj)
    d = dict()
    d['id'] = raw.group(1)
    d['name'] = raw.group(2)
    d['runtime'] = raw.group(4)
    d['status'] = raw.group(5)
    return d


def import_results(job_id, user):
    analysisJob = AnalysisJob.objects.get(external_job_id=job_id)
    dataset = Dataset.objects.get(dataset_id=analysisJob.dataset_id)
    import_data(user, open(f"{settings.PRIVATE_STORAGE_ROOT}/job_output/{job_id}_output"), datetime.datetime.now(), dataset=dataset)
