import io
import zipfile
import os
import shutil 
import geopandas as gp
from fiona.io import ZipMemoryFile
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from birdspotter.dataio.models import Dataset, Shapefile, RawData, Image, RawShapefile
import uuid

def import_new_data(user, file_path, is_public, file_name):
    """Wrapper for import_data that deals with adding new a dataset
    Args:
        user (User): Data owner
        file_path (String): File Path on system
        is_public (Boolean): Whether dataset should be public
        file_name (String): user-provided file name (used to name new dataset)
    Returns:
        True for success, False for failure
        may be worth returning other info to debug?
    """
    name = os.path.splitext(file_name)[0]
    dataset = Dataset(name=name, owner=get_user_model().objects.get_by_natural_key(user.username),
                    is_public=is_public)
    dataset.save()
    return import_data(file_path, dataset)

def import_data(file_path, dataset):
    """Takes InMemoryFile user, and dat_created and imports data into the database accordingly (creates GeoTiff or Shapefile model and 
    creates a Dataset for each file)
    Args:
        user (User): Data owner
        file_path (String): File Path on system
        dataset (Dataset): Dataset in order to use existing dataset
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
                new_path = os.path.join(settings.PRIVATE_STORAGE_ROOT, "raw_files/", str(uuid.uuid4()))
                raw_shp_data = RawData.objects.create()
                raw_shp_data.name = f"{dataset.name}"
                raw_shp_data.ext = "zip"
                raw_shp_data.path.save(new_path, io.BytesIO(binary))
                raw_shp_data.save()
                raw_shp = RawShapefile.objects.create(rawshp=raw_shp_data, dataset=dataset)
                raw_shp.save()
                return __import_shapefile(shapefile_locs, zip_mem, dataset, zip=zf)
        except zipfile.BadZipfile:
            return False
    else:
        dataset = __import_tiff(file_path, dataset)
        return dataset is not None

def __import_tiff(tiff_file, dataset):
    relative_path = f"raw_files/{str(uuid.uuid4())}"
    new_path = os.path.join(settings.PRIVATE_STORAGE_ROOT, relative_path)
    shutil.move(tiff_file, new_path)
    tiff = RawData.objects.create(path=new_path, name=f"{dataset.name}", ext="tif")
    tiff.path.name=relative_path
    tiff.save()
    dataset.geotiff=tiff
    dataset.save()
    return dataset

def __import_shapefile(file_loc, zip_mem, dataset, **kwargs):
    #2019-06-01
    if len(file_loc) > 0:
        zf=kwargs.get('zip', None)
        with zip_mem.open(file_loc[0]) as open_file:
            shp = gp.GeoDataFrame.from_features(open_file)
            shp_objects = []
            try:
                date_collected_str = shp.iloc[0]['PhotoDate']
            except KeyError:
                logging.error('PhotoDate not found, cannot generate date collected')
            for _, record in shp.iterrows():
                img = None
                if zf is not None:
                    try:
                        img_name = record.Image
                        if img_name in zf.namelist():
                            zf.extract(record.name, path='')
                            img = Image(dataset=dataset)
                            img.img_path.save(dataset.dataset_id + record.Image, zf.open(record.Image))
                            img.save()
                    except AttributeError:
                        img = None
                try:
                    shp_objects.append(Shapefile(data_set=dataset,
                                                 island_name=record.IslandName, cireg=record.CIREG,
                                                 photo_date=record.PhotoDate, observer=record.Observer,
                                                 species=record.Species,
                                                 behavior=record.Behavior, certain_p1=record.CertainP1,
                                                 comments=record.Comments if record.Comments else '',
                                                 point_x=record.geometry.x, point_y=record.geometry.y,
                                                 latitude=record.Lat, longitude=record.Long, image=img))
                except AttributeError:
                    return False
        Shapefile.objects.bulk_create(shp_objects, 100)
        dataset.date_collected = datetime.strptime(date_collected_str, '%Y-%m-%d')
        dataset.save()
        return True
    return False
