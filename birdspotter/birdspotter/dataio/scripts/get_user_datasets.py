from django.db import models
from birdspotter.accounts.models import User
from birdspotter.dataio.models import Dataset, Shapefile
import json


def get_datasets_for_user(user):
	return Dataset.objects.filter(owner_id=user.id).values()
