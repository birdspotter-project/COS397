from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class RawData(models.Model):
    """Raw data that is stored in the system, can be Zip files,
    Shapefiles, or Geotiffs that will
    be sent to the computation server

    Attributes:
        path (str): File path to file on fileserver
    """

    path = models.FileField()

class Dataset(models.Model):
    dataset_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    date_collected = models.DateField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE,
                                 null=True, blank=True)

    def __str__(self):
        return self.dataset_id + " " + self.name

