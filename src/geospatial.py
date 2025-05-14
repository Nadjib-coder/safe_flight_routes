# Module for geospatial analysis functions

import geopandas as gpd
from shapely.geometry import Point, Polygon

def is_in_dangerous_area(point, wildfire_data, volcanic_ash_data):
    point_geom = Point(point)
    for area in wildfire_data['features']:
        polygon = Polygon(area['geometry']['coordinates'][0])
        if point_geom.within(polygon):
            return True
    for area in volcanic_ash_data['features']:
        polygon = Polygon(area['geometry']['coordinates'][0])
        if point_geom.within(polygon):
            return True
    return False
