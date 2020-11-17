import geopandas as gp
from django.conf import settings
from fiona.io import ZipMemoryFile
from birdspotter.dataio.models import Dataset, Shapefile
from birdspotter.accounts.models import User
from datetime import datetime
import zipfile
import io

def import_shapefile(shapefile):
    binary = shapefile.read()
    with ZipMemoryFile(binary) as zip:
        zf = zipfile.ZipFile(io.BytesIO(binary))
        file_loc = list(filter(lambda v: v.endswith('.shp'), zf.namelist()))
        if not file_loc:
            return 'Error finding shapefile'
        with zip.open(file_loc[0]) as f:
            shp = gp.GeoDataFrame.from_features(f)
            owner = None
            if settings.DEBUG:
                owner = User.objects.get_by_natural_key('testUser')
            dataset = Dataset(name='Damaristest', is_public=True, date_created=datetime.now(), owner=owner,
                              raw_data=None, raw_data_id=None)
            dataset.save()
            shp_objects = []
            for _, record in shp.iterrows():
                shp_objects.append(Shapefile(data_set=dataset, island_name=record.IslandName, cireg=record.CIREG,
                                             photo_date=record.PhotoDate, observer=record.Observer,
                                             species=record.Species,
                                             behavior=record.Behavior, certain_p1=record.CertainP1,
                                             comments=record.Comments if record.Comments else '',
                                             point_x=record.geometry.x, point_y=record.geometry.y, latitude=record.Lat,
                                             longitude=record.Long, image=None))
            now = datetime.now()
            Shapefile.objects.bulk_create(shp_objects, 100)
            return 'Objects created successfully in %d seconds' % (now - datetime.now()).total_seconds()
