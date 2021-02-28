from birdspotter.analysis.models import AnalysisJob
import re
from pssh.clients import SSHClient
from django.conf import settings
from birdspotter.dataio.scripts.import_handler import import_data
import datetime
def handle_update(message):
    print(message.subject)
    update = parse_slurm(message.subject)
    job = AnalysisJob.objects.get(external_job_id=update['id'])
    job.status = update['status']
    job.save(update_fields='status')
    if job.status == "COMPLETED":
        import_results(settings.SLURM_HOST, settings.SLURM_USER, settings.SLURM_PASSWD, job.external_job_id, job.owner)
        print("COMPLETED job " + job.external_job_id)
def parse_slurm(subj):
    raw = re.findall(r"Slurm Job_id=(\d*) Name=([\w\d]*) (\w*), Run time ([\d:]*), (\w*), ExitCode (\d*)", subj)
    d = dict()
    d['id'] = raw.group(1)
    d['name'] = raw.group(2)
    d['runtime'] = raw.group(4)
    d['status'] = raw.group(5)
    return d
def import_results(host, user_name, password, job_id, user):
    if (not host):
        client = SSHClient(host, user=user_name, password=password)
        client.scp_recv("Documents/slurm-output-" + job_id + ".out", settings.PRIVATE_STORAGE_ROOT + "/job_output/" + job_id + "_output")
        import_data(user, open(settings.PRIVATE_STORAGE_ROOT + "/job_output/" + job_id + "_output"), datetime.datetime.now())
    else:
        print("remote: Documents/slurm-output-" + job_id + ".out" + " local: " + settings.PRIVATE_STORAGE_ROOT + "/job_output/" + job_id + "_output")
