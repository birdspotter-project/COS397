from django.db.models import Q

from birdspotter.dataio.models import Dataset
from birdspotter.dataio.models import Shapefile
from birdspotter.accounts.models import User

def get_datasets_for_user(user):
  """
  Return datasets that the user has access to, including public datasets
  """
  return Dataset.objects.filter(Q(owner_id=user.id)|Q(is_public=True)|Q(shared_with=user)).values()

def get_public_datasets():
  """
  Return public datasets for unregistered users
  """
  return Dataset.objects.filter(is_public=True).values()

def get_dataset_data(user):
    print("ISADMIN:",user)
    shapefile_lines = Shapefile.objects.filter(data_set=1)
    #Shapefile.objects.defer("species")

    if user:
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
        #return [l for l in shapefile_lines]
        return shapefile_data
    else:
        shapefile_data = {"longitude"   : [i.longitude for i in shapefile_lines],
                          "latitude"    : [i.latitude for i in shapefile_lines],
                          "island_name" : [i.island_name for i in shapefile_lines]}
        #return [l for l in shapefile_lines]
        return shapefile_data
