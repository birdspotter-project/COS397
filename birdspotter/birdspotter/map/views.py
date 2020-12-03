from django.shortcuts import render
from django.http import HttpResponse
from birdspotter.dataio.models import Dataset, Shapefile
from birdspotter.accounts.models import User
import plotly.graph_objects as go
import plotly
from django.template.response import TemplateResponse
from os import listdir
from os.path import isfile, join
import geopandas as gpd
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px


# Create your views here.

def index(request):
    '''
    '''

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
    #currently hardcoded in for testing, moves to DemarisCove directory
    #assumes a directory stored on the same level as the git directory
    #may later change to a file select for better testing
    mypath = "../../DemarisCove/Damariscov.shp"
    gdf = gpd.read_file(mypath)
    #print(gdf['IslandName'])

    #fig = go.FigureWidget(data=go.Bar(y=[2, 3, 1]))
    #graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")

    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    #print(world)
    #args['graph_div'] = plt.show()
    #x = geoplot.polyplot(world, figsize=(8, 4))

    '''
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as testURL:
        counties = json.load(testURL)
        df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})
        #print(df)
        #print("\n"*10)
        #print(gdf)
        fig = px.choropleth_mapbox(df, geojson=None, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=10, center = {"lat": 43.779, "lon": -69.61},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        #fig.show()
    '''
    #args['graph_div'] = graph_div

    args['isAdmin'] = False
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

    #px.set_mapbox_access_token(open(".mapbox_token").read())
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

    #return render(request, 'base.html')
