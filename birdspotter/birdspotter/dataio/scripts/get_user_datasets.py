from birdspotter.dataio.models import Dataset
from birdspotter.dataio.models import Shapefile

def get_datasets_for_user(user):
    """Gets all datasets owned by user
    """
    return Dataset.objects.filter(owner_id=user.id).values()


def get_public_datasets():
    """Gets all public datasets
    """
    return Dataset.objects.filter(is_public=True).values()


def get_dataset_data(is_authed, uuid):
    dataset = Dataset.objects.get(dataset_id=uuid)
    shapefile_lines = Shapefile.objects.filter(data_set=dataset.id)
    #Shapefile.objects.defer("species")

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
        #return [l for l in shapefile_lines]
        return shapefile_data
    shapefile_data = {"longitude"   : [i.longitude for i in shapefile_lines],
                      "latitude"    : [i.latitude for i in shapefile_lines],
                      "island_name" : [i.island_name for i in shapefile_lines]}
    #return [l for l in shapefile_lines]
    return shapefile_data
