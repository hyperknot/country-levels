from country_level_lib.config import (
    id_dir,
    geojson_dir,
    export_id0_dir,
    export_id1_dir,
    export_id2_dir,
)
from country_level_lib.utils import read_json, write_json


def export_id0():
    levels = read_json(id_dir / 'id012.json')
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

        export_id0_dir.mkdir(exist_ok=True, parents=True)
        write_json(geojson_path, feature_data)

    print(f'{len(countries)} id0 GeoJSONs exported')


def export_id1():
    levels = read_json(id_dir / 'id012.json')
    units = read_json(geojson_dir / 'units.geojson')['features']

    features_by_id = {}

    for feature in units:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)
        ne_id = prop['ne_id']
        features_by_id[ne_id] = feature

    counter = 0
    for id0, id0_data in levels.items():
        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            ne_id = id1_data['ne_id']
            feature_data = features_by_id[ne_id]

            # skip one-to-one fixed polygons
            if id1[:3] == 'id0':
                continue

            filename = id1[4:].lower()
            geojson_path = export_id1_dir / f'{filename}.geojson'

            export_id1_dir.mkdir(exist_ok=True, parents=True)
            write_json(geojson_path, feature_data)

            counter += 1

    print(f'{counter} id1 GeoJSONs exported')


def export_id2():
    levels = read_json(id_dir / 'id012.json')
    subunits = read_json(geojson_dir / 'subunits.geojson')['features']

    features_by_id = {}

    for feature in subunits:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)
        ne_id = prop['ne_id']
        features_by_id[ne_id] = feature

    counter = 0
    for id0, id0_data in levels.items():
        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            if 'sub2' not in id1_data:
                continue

            sub2 = id1_data['sub2']
            for id2, id2_data in sub2.items():
                ne_id = id2_data['ne_id']
                feature_data = features_by_id[ne_id]

                filename = id2[4:].lower()
                geojson_path = export_id2_dir / f'{filename}.geojson'

                export_id2_dir.mkdir(exist_ok=True, parents=True)
                write_json(geojson_path, feature_data)

                counter += 1

    print(f'{counter} id2 GeoJSONs exported')
