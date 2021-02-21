from django.conf import settings
from django.db import models
import uuid
from birdspotter.dataio.models import RawData, Dataset

# Create your models here.
class AnalysisJob(models.Model):
    """Status and related information for Job queued on external compute

    Attributes:
        owner (User): User who queued the analysis

    """
    status = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    job_id = models.UUIDField(primary_key=False,
                                default=uuid.uuid4,
                                editable=False, unique=True)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(auto_now_add=False)
    input_data = models.ForeignKey(RawData, on_delete=models.CASCADE)
    output_data = models.ForeignKey(RawData, on_delete=models.CASCADE,
                                 null=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)