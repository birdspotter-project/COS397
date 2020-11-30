from django.db import models
from django.conf import settings


class Image(models.Model):
    img_path = models.FileField()


class RawData(models.Model):
    path = models.FileField()


class Dataset(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    date_collected = models.DateField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE, null=True, blank=True)


class Shapefile(models.Model):
    data_set = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    island_name = models.CharField(max_length=50)
    cireg = models.CharField(max_length=20)
    photo_date = models.DateField()
    observer = models.CharField(max_length=50)
    species = models.CharField(max_length=100)
    behavior = models.IntegerField()
    certain_p1 = models.CharField(max_length=20)
    comments = models.CharField(max_length=500, blank=True)
    point_x = models.FloatField()
    point_y = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
