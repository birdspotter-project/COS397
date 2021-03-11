from django.shortcuts import render
import geopandas as gpd
import plotly
import plotly.express as px
import numpy as np
import pandas as pd
from birdspotter.dataio.scripts.get_user_datasets import get_dataset_data

def index(request, uuid):
    """
    base function for the Map View handling, checks permissions of the user and dispatches to other functions
    """

    args = {}

    shapefile_lines = get_dataset_data(request.user.is_authenticated, uuid)


    df = pd.DataFrame({})
    #populate DataFrame
    for key in shapefile_lines:
        df[key] = shapefile_lines[key]
    #create corresponding GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    
    plot = create_map(request.user.is_authenticated, gdf)
    args['graph_div'] = plot
    
    return render(request, 'map.html', args)


def create_map(is_admin, gdf):
    """
    return a figure from plotly.offline.plot
    """


    fields = {"lon":gdf.longitude, "lat":gdf.latitude, "species":gdf.species}


    zoom, center = zoom_center(lons=fields["lon"], lats=fields["lat"]) #zoom to fit data
    if is_admin:
        #should have data retreived on backend to be consistent
        fig = make_point_map(gdf, zoom, center, fields)
    else:
        #need to hide data on backend, not client-side
        fig = make_bubble_map(gdf, zoom, center, fields)      


    fig.update_layout(margin={"r":0,"l":0,"b":0,"t":0})
    #fig = fig.to_image(format="png", width=600, height=350, scale=2)
    return plotly.offline.plot(fig, auto_open = False, output_type="div", config={'displayModeBar': False})


def make_point_map(gdf, zoom, center, fields):
    """
    to be called for the registered user, displays all individual points and bird species
    """
    fig = px.scatter_mapbox(gdf, lat=fields["lat"], lon=fields["lon"], 
                            hover_name=fields["species"], hover_data=[],
                            color_discrete_sequence=["red"], zoom=zoom, center=center)
    fig.update_layout(mapbox_style="white-bg",
                      mapbox_layers=[
                          {
                              "below": 'traces',
                              "sourcetype": "raster",
                              "source": [
                                  "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                              ]
                          }
                      ])
    return fig


def make_bubble_map(gdf, zoom, center, fields):
    """
    to be called fot the non-registered user, should display aggregated points with no species info
    the gdf should be modified such that it only has info on lat/long, and concentration.
    """
    fig = px.scatter_mapbox(gdf, lat=fields["lat"], lon=fields["lon"], 
                            hover_name=fields["species"], hover_data=[],
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
    return fig


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
    #from https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps

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
