from django.test import TestCase
import pandas as pd
from birdspotter.map import views
# Create your tests here. test functions must start with test_

class MapViewTests(TestCase):
    """
    Testing set for the Map View
    Functions: test_missing_field, test_empty_field, test_
    """
    
    def create_gdf(self, fields):
        """
        create a geodataframe with the given fields and types of the values for the fields
        """
        df = pd.DataFrame({})
        return
        
    def test_bad_field(self):
        """
        check that field formats that are unexpected are properly handled
        ie) if there is a string in a lat/long section, it should not attempt to display
        points on a map
        """
        return
    def test_empty_field(self):
        """
        check that the code works properly when the there is no data in a field whatsoever
        Fields of gdf from DamarisCove are: 
        IslandName, CIREG, PhotoDate, Observer, Species, Behavior, 
        CertainP1, BehaviorP2, Comments, POINT_X, POINT_Y, Lat, Long, geometry.
        
        of these, most should be visible if wanted for a registered user.
        """
        return    
        
    def test_missing_field(self):
        """
        check that the code works properly when there is a field missing from the shapefile
        ie) missing species may affect the make_point_map function
        """
        
        df = pd.DataFrame({'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
            'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
            'Lat': [-34.58, -15.78, -33.45, 4.60, 10.48],
            'Long': [-58.66, -47.91, -70.66, -74.08, -66.86]})
        gdf = views.gpd.GeoDataFrame(df, geometry = views.gpd.points_from_xy(df.Long, df.Lat))
        print(gdf.head())
        return
       
    def test_bubble_admin(self):
        """ check that make_bubble_map is not called with isAdmin = True
            may be liable to change if adding display options in admin view"""
        return
    
    def test_point_admin(self):
        """check that make_point_map not called without isAdmin = True"""
        return