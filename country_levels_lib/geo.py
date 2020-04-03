from shapely.geometry import shape
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()


def calculate_centroid(feature):
    geom = shape(feature['geometry'])
    centroid = geom.centroid
    return {'lat': centroid.y, 'lon': centroid.x}


def find_timezone(lon, lat):
    return tf.timezone_at(lng=lon, lat=lat)
