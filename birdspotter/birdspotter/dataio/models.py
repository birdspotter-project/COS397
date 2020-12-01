"""All models related to data portrayed by the system for visualizations and analysis
"""
from django.conf import settings
from django.db import models


class Image(models.Model):
    """Image that will be stored in fileserver and referenced in map view
    
    Attributes:
        img_path (str): File path to image in fileserver
    """

    img_path = models.FileField()


class RawData(models.Model):
    """Raw data that is stored in the system, can be Zip files, Shapefiles, or Geotiffs that will
    be sent to the computation server
    
    Attributes:
        path (str): File path to file on fileserver
    """

    path = models.FileField()


class Dataset(models.Model):
    """Dataset object that is created either by importing a shapefile, or from resulting analysis
    
    Attributes:
        date_collected (datetime.date): Date when the data was collected
        date_created (datetime.datetime): Datetime when the dataset was uploaded to the system
        is_public (bool): If the dataset can be seen by all users
        name (str): Dataset name
        owner (User): User who uploaded and is responsible for the dataset
        raw_data (RawData): ForeignKey to dataio.RawData
    """

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    date_collected = models.DateField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE, null=True, blank=True)


class Shapefile(models.Model):
    """Database implementation of a Shapefile row
    
    Attributes:
        behavior (int): Boolean value of whether bird is nesting or not
        certain_p1 (TYPE): Certainty of identification (Y-> Certain, NB-> unknown behavior, NS-> Unknown species)
        cireg (str): Island registration number
        comments (str): Observer comments
        data_set (Dataset): ForeignKey to dataio.Dataset
        image (Image): ForeignKey to dataio.Image
        island_name (str): Island name
        latitude (float): Latitude
        longitude (float): Longitude
        observer (string): Name of observer
        photo_date (date): Date of photo
        point_x (float): x coordinate in relation to raster image
        point_y (float): y coordinate in relation to raster image
        species (str): bird species
    """

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
