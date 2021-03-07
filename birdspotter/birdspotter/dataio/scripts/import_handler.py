import io
import re
import zipfile
import os
import shutil 
import uuid
import geopandas as gp
from fiona.io import ZipMemoryFile
from django.conf import settings
from birdspotter.accounts.models import User
from birdspotter.dataio.models import Dataset, Shapefile, RawData, Image


def import_data(user, file_path, file_name, date_created):
    """Takes InMemoryFile user, and dat_created and imports data into the database accordingly (creates GeoTiff or Shapefile model and 
    creates a Dataset for each file)
    Args:
        user (User): Data owner
        user_file (InMemoryFile): Description
        date_created (datetime.date): Description

    Returns:
        True for success, False for failure
        may be worth returning other info to debug?
    """
    if zipfile.is_zipfile(file_path):
        binary = open(file_path, 'rb').read()
        try:
            with ZipMemoryFile(binary) as zip_mem:
                zf = zipfile.ZipFile(io.BytesIO(binary))
                shapefile_locs = list(filter(lambda v: v.endswith('.shp'), zf.namelist()))
                return import_shapefile(shapefile_locs, zip_mem, user, date_created, zip=zf)
        except zipfile.BadZipfile:
            return False
    else :
        dataset = import_tiff(file_path, file_name, user, date_created)
        return dataset is not None
def import_tiff(tiff_file, file_name, user, date_created):
    new_path = os.path.join(settings.PRIVATE_STORAGE_ROOT, f"raw_files/{uuid.uuid1()}")
    shutil.move(tiff_file, new_path)
    tiff = RawData.objects.create(path=new_path)
    name = re.findall(r"(\w+).tif", file_name)[0]
    dataset = Dataset(name=name, owner=User.objects.get_by_natural_key(user.username),
                              date_collected=date_created, geotiff=tiff)
    dataset.save()
    return dataset
def import_shapefile(file_loc, zip_mem, user, date_created, **kwargs):
    if len(file_loc) > 0:
        file_name = re.findall(r"(\w+).shp", file_loc[0])[0]
        print(file_name)
        dataset = kwargs.get('dataset', None)
        if dataset is None : 
            dataset = Dataset(name=file_name, owner=User.objects.get_by_natural_key(user.username),
                              date_collected=date_created)
        dataset.save()
        zf=kwargs.get('zip', None)
        with zip_mem.open(file_loc[0]) as open_file:
            shp = gp.GeoDataFrame.from_features(open_file)
            shp_objects = []
            for _, record in shp.iterrows():
                img = None
                if zf is not None :
                    try:
                        img_name = record.Image
                        if img_name in zf.namelist():
                            zf.extract(record.name, path='')
                            img = Image(dataset=dataset)
                            img.img_path.save(dataset.dataset_id + record.Image, zf.open(record.Image))
                            img.save()
                    except AttributeError:
                        img = None
                shp_objects.append(Shapefile(data_set=dataset,
                                             island_name=record.IslandName, cireg=record.CIREG,
                                             photo_date=record.PhotoDate, observer=record.Observer,
                                             species=record.Species,
                                             behavior=record.Behavior, certain_p1=record.CertainP1,
                                             comments=record.Comments if record.Comments else '',
                                             point_x=record.geometry.x, point_y=record.geometry.y,
                                             latitude=record.Lat, longitude=record.Long, image=img))
        Shapefile.objects.bulk_create(shp_objects, 100)
        return True
    return False