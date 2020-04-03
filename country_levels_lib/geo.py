from shapely.geometry import shape


def calculate_centroid(feature):
    geom = shape(feature['geometry'])
    centroid = geom.centroid
    return {'lat': centroid.y, 'lon': centroid.x}


