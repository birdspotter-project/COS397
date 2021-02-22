from django.conf import settings
from django.db import models
import uuid
from birdspotter.dataio.models import RawData, Dataset, RawShapefile

# Create your models here.
class Algorithm(models.Model):
    name = models.CharField(max_length=50)
    algo_id = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False, unique=True)
    def __str__(self):
        return self.name
    file_name = models.FileField()
class AnalysisJob(models.Model):
    """Status and related information for Job queued on external compute

    Attributes:
        owner (User): User who queued the analysis
        status (<50 Chars): Current status of job (queuing, waiting, done, failed, etc)
        date_started (DateTime): Date and time of when the job was queued
        date_finished (DateTime): Date and time of when the job process was completed
        input_data (RawData): GeoTiff input
        output_data (RawShapefile): Raw shapefile data
        dataset (Dataset): associated dataset
        algorithm (Algorithm): algorithm to be used in analysis
    """
    status = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    job_id = models.UUIDField(primary_key=False,
                                default=uuid.uuid4,
                                editable=False, unique=True)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(auto_now_add=False)
    input_data = models.ForeignKey(RawData, related_name='uses',on_delete=models.SET_NULL,null=True)
    output_data = models.ForeignKey(RawShapefile, related_name='creates',on_delete=models.SET_NULL,
                                 null=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    algorithm_used = models.ForeignKey(Algorithm, to_field='algo_id', on_delete=models.SET_NULL,null=True)