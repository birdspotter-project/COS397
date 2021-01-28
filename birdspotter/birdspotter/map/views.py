from birdspotter.dataio.models import Dataset, Shapefile
from birdspotter.dataio.scripts.get_user_datasets import *
import plotly
from django.template.response import TemplateResponse
import geopandas as gpd
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

def index(request):
    '''
    '''

    datasets = get_datasets_for_user(request.user)
    args = {}
    columns = ['IslandName', 'CIREG', 'PhotoDate', 'Observer', 'Species', 'Behavior', 'CertainP1',
                        'BehaviorP2', 'Comments', 'POINT_X', 'POINT_Y', 'Lat', 'Long', 'geometry']
    '''
    IslandName      object
    CIREG           object
    PhotoDate       object
    Observer        object
    Species         object
    Behavior        object
    CertainP1       object
    BehaviorP2      object
    Comments        object
    POINT_X        float64
    POINT_Y        float64
    Lat            float64
    Long           float64
    '''
    #currently hardcoded in for testing, moves to DemarisCove directory. 
    #expects directory to be on the same level as Repo base folder.
<<<<<<< HEAD
    mypath = "../../Damariscove/Damariscov.shp"
=======
    mypath = "../../DamarisCove/Damariscov.shp"
>>>>>>> 9caf4ff3deddd6d91d539eb8efc51a03c0faa128
    gdf = gpd.read_file(mypath)

    args['isAdmin'] = False
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

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
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(width=1900)
    fig.update_layout(height=800)

    args['graph_div'] = plotly.offline.plot(fig, auto_open = False, output_type="div")

    return TemplateResponse(request, 'map.html', args)
