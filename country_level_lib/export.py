from country_level_lib.config import levels_dir, geojson_dir, export_id0_dir
from country_level_lib.utils import read_json, write_json


def export_0():
    levels = read_json(levels_dir / 'level_012.json')
    countries = read_json(geojson_dir / 'countries.geojson')['features']

    features_by_id = {}

    for feature in countries:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)
        ne_id = prop['ne_id']
        features_by_id[ne_id] = feature

    for id0, data in levels.items():
        ne_id = data['ne_id']
        feature_data = features_by_id[ne_id]

        filename = id0[4:].lower()
        geojson_path = export_id0_dir / f'{filename}.geojson'
        export_id0_dir.mkdir(exist_ok=True)

        write_json(geojson_path, feature_data)

    print(f'{len(levels)} level_0 geojson exported')
