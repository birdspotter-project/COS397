import io
import re
import zipfile

import geopandas as gp
from django.conf import settings
from fiona.io import ZipMemoryFile

from birdspotter.accounts.models import User
from birdspotter.dataio.models import Dataset, Shapefile


def import_shapefile(request, shapefile, date_created):
    """Takes InMemoryFile and form data (date_created) as imports data into Shapefile model and 
    creates a Dataset for each file

    Args:
        shapefile (InMemoryFile): Description
        date_created (datetime.date): Description

    Returns:
        True for success, False for failure
        may be worth returning other info to debug?
        """
    binary = shapefile.read()
    try:
        with ZipMemoryFile(binary) as zip_mem:
            zf = zipfile.ZipFile(io.BytesIO(binary))
            file_loc = list(filter(lambda v: v.endswith('.shp'), zf.namelist()))
            if len(file_loc) > 0:
                with zip_mem.open(file_loc[0]) as open_file:
                    shp = gp.GeoDataFrame.from_features(open_file)
                    file_name = re.findall(r"(\w+).shp", file_loc[0])[0]
                    owner = User.objects.get_by_natural_key(request.user.username)
                    dataset = Dataset(name=file_name, is_public=True, owner=owner,
                                      date_collected=date_created, raw_data=None, raw_data_id=None)
                    dataset.save()
                    shp_objects = []
                    for _, record in shp.iterrows():
                        shp_objects.append(Shapefile(data_set=dataset,
                                                     island_name=record.IslandName, cireg=record.CIREG,
                                                     photo_date=record.PhotoDate, observer=record.Observer,
                                                     species=record.Species,
                                                     behavior=record.Behavior, certain_p1=record.CertainP1,
                                                     comments=record.Comments if record.Comments else '',
                                                     point_x=record.geometry.x, point_y=record.geometry.y,
                                                     latitude=record.Lat, longitude=record.Long, image=None))
                Shapefile.objects.bulk_create(shp_objects, 100)
        return True
    except zipfile.BadZipfile:
        return False
        #print("Failed to upload")
