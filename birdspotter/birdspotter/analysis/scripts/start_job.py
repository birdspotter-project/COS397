from birdspotter.analysis.models import Algorithm
from birdspotter.dataio.models import Dataset
def start_job(request, algorithm, uuid):
    """Start 
    Args:
        
    Returns:
        Status of queuing job
    """
    algo = Algorithm.object.get(algo_id=algorithm)
    dataset = Dataset.objects.get(dataset_id=uuid)
    print(dataset.owner,algo.file_name)
    return False