from django.db.models import Q

from birdspotter.dataio.models import Dataset
from birdspotter.dataio.models import Shapefile
import logging


def get_datasets_for_user(user):
    """
    Return datasets that the user has access to, including public datasets
    """
    return Dataset.objects.filter(Q(owner_id=user.id) | Q(is_public=True) | Q(shared_with=user)).distinct().values()


def get_public_datasets():
    """
    Return public datasets for unregistered users
    """
    return Dataset.objects.filter(is_public=True).values()


def get_dataset_data(is_authed, uuid):
    """
    Arguments:
        is_authed (bool):   true for registered users
        uuid (dataset id)
    """
    lat_min = None
    lat_max = None
    lon_min = None
    lon_max = None
    dataset = Dataset.objects.get(dataset_id=uuid)
    shapefile_lines = Shapefile.objects.filter(data_set=dataset.id)
    if not shapefile_lines.exists():
        logging.error("no shape lines")
        return None
    shapefile_data = {}

    if is_authed:
        shapefile_data = {"longitude"   : [i.longitude for i in shapefile_lines],
                          "latitude"    : [i.latitude for i in shapefile_lines],
                          "island_name" : [i.island_name for i in shapefile_lines],
                          "species"     : [i.species for i in shapefile_lines],
                          "cireg"       : [i.cireg for i in shapefile_lines],
                          "photo_date"  : [i.photo_date for i in shapefile_lines],
                          "observer"    : [i.observer for i in shapefile_lines],
                          "behavior"    : [i.behavior for i in shapefile_lines],
                          "certain_p1"  : [i.certain_p1 for i in shapefile_lines],
                          "comments"    : [i.comments for i in shapefile_lines],
                          }
    else:
        precision = 1       # aggregate data to 1 decimals points of lat/long
        precision_mod = 1  # allows for more precise tuning, >1 reduces region size <1 increases region size
        aggregation = {}

        for i in shapefile_lines:
            # separate by island name and by precision,
            # in case there are multiple islands in one dataset
            if lat_min is None:
                lat_min = i.latitude
                lat_max = i.latitude
                lon_min = i.longitude
                lon_max = i.longitude
            
            lat_min = min(lat_min, i.latitude)
            lat_max = max(lat_max, i.latitude)
            lon_min = min(lon_min, i.longitude)
            lon_max = max(lon_max, i.longitude)
            
            key = (round(i.latitude*precision_mod, precision),
                round(i.longitude*precision_mod, precision),
                i.island_name)
            if key in aggregation:
                aggregation[key][0] += i.latitude
                aggregation[key][1] += i.longitude
                aggregation[key][2] += 1
            else:
                aggregation[key] = [i.latitude, i.longitude, 1, i.island_name]

        for key in aggregation:
            # average data region, to 4 decimal precision
            aggregation[key][0] = round(aggregation[key][0]/aggregation[key][2], 4)
            aggregation[key][1] = round(aggregation[key][1]/aggregation[key][2], 4)

        shapefile_data = {"latitude"    : [aggregation[key][0] for key in aggregation],
                          "longitude"   : [aggregation[key][1] for key in aggregation],
                          "island_name" : [aggregation[key][3] for key in aggregation],
                          "size"       : [aggregation[key][2] for key in aggregation]}

    return shapefile_data, dataset.name, {"lat_bounds": (lat_min, lat_max), "lon_bounds": (lon_min, lon_max)}
