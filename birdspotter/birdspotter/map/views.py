#from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
import plotly
from django.template.response import TemplateResponse
import geopandas as gpd
import plotly.express as px
import numpy as np

def index(request):
    '''
    '''

    #datasets = get_datasets_for_user(request.user)
    args = {}
    #currently hardcoded in for testing, moves to DemarisCove directory. 
    #expects directory to be on the same level as Repo base folder.
    mypath = "../../DemarisCove/Damariscov.shp"
    gdf = gpd.read_file(mypath)

    args['isAdmin'] = False
    
    if args['isAdmin']:
        fig = px.scatter_mapbox(gdf, lat="Lat", lon="Long", hover_name="Species", hover_data=[],
                                color_discrete_sequence=["red"], zoom=3, height=300)
        fig.update_layout(mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])
    else:
        #need to hide data on backend, not client-side
        zoom, center = zoom_center(lons=gdf.Long, lats=gdf.Lat) #set the appropriate zoom default
        fig = px.scatter_mapbox(gdf, lat="Lat", lon="Long", hover_name="Species", hover_data=[],
                                color_discrete_sequence=["red"], zoom=zoom, center= center)
        fig.update_layout(mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])
        
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    fig.update_layout(height=742)
    args['graph_div'] = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return TemplateResponse(request, 'map.html', args)

#from https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
def zoom_center(lons: tuple = None, lats: tuple = None, 
        projection: str = 'mercator',
        width_to_height: float = 2.0) -> (float, dict):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434
    
    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.
    
    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys

    >>> print(zoom_center((-109.031387, -103.385460),
    ...     (25.587101, 31.784620)))
    (5.75, {'lon': -106.208423, 'lat': 28.685861})
    """
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    #center = 
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    if projection == 'mercator':
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            f'{projection} projection is not implemented'
        )
    
    return zoom, {'lon': round((maxlon + minlon) / 2, 6), 'lat': round((maxlat + minlat) / 2, 6)}