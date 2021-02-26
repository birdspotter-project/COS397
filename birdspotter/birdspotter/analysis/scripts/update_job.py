from birdspotter.analysis.models import AnalysisJob
import re
def handle_update(message):
    print(message.subject)
    update = parse_slurm(message.subject)
    job = AnalysisJob.objects.get(external_job_id=update['id'])
    job.status = update['status']
    job.save(update_fields=['status'])
    if job.status == "COMPLETED":
        # scp over files
        # import shapefiles into app
        print("COMPLETED job " + job.external_job_id)
def parse_slurm(subj):
    raw = re.findall(r"Slurm Job_id=(\d*) Name=([\w\d]*) (\w*), Run time ([\d:]*), (\w*), ExitCode (\d*)", subj)
    d = dict()
    d['id'] = raw.group(1)
    d['name'] = raw.group(2)
    d['runtime'] = raw.group(4)
    d['status'] = raw.group(5)
    return d
