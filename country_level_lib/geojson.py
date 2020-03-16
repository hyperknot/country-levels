from country_level_lib.config import id_dir, geojson_dir, export_id0_dir, export_id1_dir
from country_level_lib.utils import read_json, write_json


def export_0():
    levels = read_json(id_dir / 'level_012.json')
    countries = read_json(geojson_dir / 'countries.geojson')['features']

    features_by_id = {}

    for feature in countries:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)
        ne_id = prop['ne_id']
        features_by_id[ne_id] = feature

    for id0, id0_data in levels.items():
        ne_id = id0_data['ne_id']
        feature_data = features_by_id[ne_id]

        filename = id0[4:].lower()
        geojson_path = export_id0_dir / f'{filename}.geojson'

        export_id0_dir.mkdir(exist_ok=True)
        write_json(geojson_path, feature_data)

    print(f'{len(countries)} id0 geojson exported')


def export_1():
    levels = read_json(id_dir / 'level_012.json')
    units = read_json(geojson_dir / 'units.geojson')['features']

    features_by_id = {}

    for feature in units:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)
        ne_id = prop['ne_id']
        features_by_id[ne_id] = feature

    for id0, id0_data in levels.items():
        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            ne_id = id1_data['ne_id']
            feature_data = features_by_id[ne_id]

            filename = id1[4:].lower()
            geojson_path = export_id1_dir / f'{filename}.geojson'

            export_id1_dir.mkdir(exist_ok=True)
            write_json(geojson_path, feature_data)

    print(f'{len(units)} id1 geojson exported')
