from birdspotter.analysis.models import AnalysisJob
from birdspotter.dataio.models import Dataset
from pssh.clients import SSHClient
import re
from django.conf import settings
def start_job(request, algo, uuid):
    """Start 
    Args:
        
    Returns:
        Status of queuing job
    """
    dataset = Dataset.objects.get(dataset_id=uuid)
    if dataset.geotiff is None :  # Ensure that the dataset has a geotiff associated
        return False
    job = AnalysisJob(status="LOADING", owner=request.user, dataset=dataset, algorithm_used=algo, input_data=dataset.geotiff)
    job.save()
    if not settings.SLURM_HOST: 
        client = SSHClient(settings.SLURM_HOST, user=settings.SLURM_USER, password=settings.SLURM_PASSWD)
        client.scp_send(algo.file_name.path, "birdspotter_auto_script")
        client.run_command("chmod +x birdspotter_auto_script")
        cmd = get_slurm_cmd(settings.SLURM_USER, settings.EMAIL_HOST_USER, settings.SLURM_OPTS, settings.DO_CONDA) + " ./birdspotter_auto_script"
        print("Command: " + cmd)
        output = client.run_command(cmd)
        for line in output.stdout:
            print("output: " + line)
            if re.match(r"job (\d*)", line):
                job.external_job_id = re.findall(r"job (\d*)", line).group(1)
                job.save(update_fields='external_job_id')
        for line in output.stderr:
            print("error: " + line)
    else:
        print(algo.file_name.path + " " +  settings.SLURM_USER + " " + settings.EMAIL_HOST_USER + " " + settings.SLURM_OPTS)
    return True
def get_slurm_cmd(user_name, email, special_opts, do_conda):
    conda_activate = ""
    if do_conda.lower() == 'true':
        conda_activate = "conda activate " + user_name + " && "
    srun_base = "srun " + special_opts + " --mail-type=BEGIN,END,FAIL,TIME_LIMIT"
    email_def = " --mail-user=" + email
    error_def = " --error=/home/" + user_name + "/Documents/slurm-error-%j.out"
    output_def = " --output=/home/" + user_name + "/Documents/slurm-output-%j.out"
    return conda_activate + srun_base + email_def + error_def + output_def 
