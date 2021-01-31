from birdspotter.dataio.scripts.get_user_datasets import get_datasets_for_user
import plotly
from django.template.response import TemplateResponse
import geopandas as gpd
import plotly.express as px

def index(request):
    '''
    '''

    datasets = get_datasets_for_user(request.user)
    args = {}
    #currently hardcoded in for testing, moves to DemarisCove directory. 
    #expects directory to be on the same level as Repo base folder.
    mypath = "../../DemarisCove/Damariscov.shp"
    gdf = gpd.read_file(mypath)

    args['isAdmin'] = False

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
