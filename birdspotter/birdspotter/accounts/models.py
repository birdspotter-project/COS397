from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list
from birdspotter.dataio.models import Dataset


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    data_sets = models.ManyToManyField(Dataset)