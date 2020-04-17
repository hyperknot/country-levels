import shutil

from country_levels_lib.config import geojson_dir, export_dir
from country_levels_lib.fips.fips_utils import get_state_data, get_county_data
from country_levels_lib.geo import calculate_centroid, find_timezone
from country_levels_lib.utils import read_json, write_json

fips_geojson_dir = geojson_dir / 'fips'


quality_map = {
    'low': '20m',
    'medium': '5m',
    'high': '500k',
}


def export_fips():
    for quality in quality_map:
        process_fips_quality(quality)


def process_fips_quality(quality):
    assert quality in [5, 7, 8]

    print(f'Processing FIPS county GeoJSON {quality_map[quality]}')

    features = read_json(fips_geojson_dir / f'counties_{quality_map[quality]}.geojson')['features']

    counties_by_str = get_county_data()[1]
    states_by_int = get_state_data()[0]

    geojson_export_dir = export_dir / 'geojson' / f'q{quality}' / 'fips'
    shutil.rmtree(geojson_export_dir, ignore_errors=True)

    new_features = list()
    json_data = dict()

    count = 0
    for feature in features:
        prop = feature['properties']
        full_code_str = prop['GEOID']
        state_code_int = int(prop['STATEFP'])
        county_code = int(prop['COUNTYFP'])

        # skip minor islands without state code found in 500k dataset
        if state_code_int not in states_by_int:
            continue

        centroid = calculate_centroid(feature)
        timezone = find_timezone(centroid['lon'], centroid['lat'])

        county_data = counties_by_str[full_code_str]
        assert county_data['county_code'] == county_code
        assert county_data['state_code_int'] == state_code_int

        name = county_data['name']
        name_long = county_data['name_long']

        state_code_int = county_data['state_code_int']
        state_code_postal = county_data['state_code_postal']
        state_code_iso = county_data['state_code_iso']

        population = county_data['population']

        countrylevel_id = f'fips:{full_code_str}'

        for key in ['NAME', 'GEOID', 'STATEFP', 'COUNTYFP']:
            del prop[key]

        new_prop = {
            'name': name,
            'name_long': name_long,
            'fips': full_code_str,
            'state_code_int': state_code_int,
            'state_code_postal': state_code_postal,
            'state_code_iso': state_code_iso,
            'county_code': county_code,
            'population': population,
            'countrylevel_id': countrylevel_id,
            'census_data': prop,
            'center_lat': round(centroid['lat'], 2),
            'center_lon': round(centroid['lon'], 2),
            'timezone': timezone,
        }
        feature['properties'] = new_prop
        new_features.append(feature)

        state_code_str = full_code_str[:2]
        state_subdir = geojson_export_dir / state_code_str
        state_subdir.mkdir(parents=True, exist_ok=True)
        write_json(state_subdir / f'{full_code_str}.geojson', feature)
        count += 1

        json_data[full_code_str] = {k: v for k, v in new_prop.items() if k != 'census_data'}
        json_data[full_code_str]['geojson_path'] = f'fips/{state_code_str}/{full_code_str}.geojson'

    write_json(
        export_dir / 'geojson' / f'q{quality}' / 'fips_all.geojson',
        {"type": "FeatureCollection", "features": new_features},
    )

    if quality == 7:  # only write the file once
        write_json(export_dir / f'fips.json', json_data, indent=2, sort_keys=True)

    assert count == len(counties_by_str)
    print(f'  {count} GeoJSON processed')
