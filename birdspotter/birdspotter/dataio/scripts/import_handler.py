import geopandas as gp
from fiona.io import ZipMemoryFile
from django.conf import settings


def import_shapefile(shapefile):
    binary = shapefile.read()
    with ZipMemoryFile(binary) as zip:
        with zip.open('Damariscove/Damariscov.shp') as f:
            shp = gp.GeoDataFrame.from_features(f)
            return shp.Species.unique()

