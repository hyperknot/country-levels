from country_levels_lib.config import fixes_dir
from country_levels_lib.utils import read_json


def get_osm_missing_features():
    osm_missing_dir = fixes_dir / 'osm_missing'
    geojson_paths = osm_missing_dir.glob('*.geojson')

    features = []
    for geojson_path in geojson_paths:
        geojson = read_json(geojson_path)
        if geojson['type'] == 'Feature':
            clean_tags_overpass(geojson)
            features.append(geojson)
        if geojson['type'] == 'FeatureCollection':
            for feature in geojson['features']:
                clean_tags_overpass(feature)
                features.append(feature)

    return features


def clean_tags_overpass(feature):
    props = feature['properties']
    props['id'] = int(props.pop('@id').split('/')[1])

    keys_to_alltags = ['ISO3166-1', 'ISO3166-2']
    keys_to_alltags.extend({k for k in props.keys() if k.startswith('name:')})

    alltags = {}
    for key in keys_to_alltags:
        if key in props:
            alltags[key] = props.pop(key)

    props['alltags'] = alltags
