from django.test import TestCase
from birdspotter.map import views
import pandas as pd
# Create your tests here. test functions must start with test_

class MapViewTests(TestCase):
    """
    Testing set for the Map View
    Functions: 
    """
    
    def create_gdf(self, fields):
        """
        create a geodataframe with the given fields and types of the values for the fields
        """
        
        return
    def test_empty_field(self):
        """
        """
        return    
        
    def test_missing_field(self):
        df = pd.DataFrame({'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Lat': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Long': [-58.66, -47.91, -70.66, -74.08, -66.86]})
        gdf = views.gpd.GeoDataFrame(df, geometry = views.gpd.points_from_xy(df.Long, df.Lat))
        print(gdf.head())
        return
       
    
    #test that fields match what is required  
    #Fields of gdf from DamarisCove: IslandName, CIREG, PhotoDate, Observer, Species, Behavior, CertainP1, BehaviorP2, Comments, POINT_X, POINT_Y, Lat, Long, geometry
    
    #Check that isAdmin value is valid
    
    #check that make_point_map not called without isAdmin = True
    #also maybe a reminder to add multiple user types (isRegistered, isPrivileged)?
    
    #check that make_bubble_map is only called when isAdmin = False