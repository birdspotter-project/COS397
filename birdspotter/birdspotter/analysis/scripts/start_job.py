from birdspotter.analysis.models import AnalysisJob
from birdspotter.dataio.models import Dataset
from django.conf import settings
import os
import logging


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
    analysis_string = f"{algo.file_name.path},{dataset.geotiff.path},{os.path.join(settings.PRIVATE_STORAGE_ROOT, 'tmp/')}"
    logging.info(analysis_string)
    return True
