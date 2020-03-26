import csv

from country_levels_lib.config import data_dir, geojson_dir
from country_levels_lib.utils import read_json, write_json

fips_data_dir = data_dir / 'fips'
fips_csv = fips_data_dir / 'fips.csv'
fips_geojson_dir = geojson_dir / 'fips'


def get_census_dicts():
    rows = list()

    with open(fips_csv, newline='') as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=[
                'summary_level',
                'state_code',
                'county_code',
                'county_subdivision_code',
                'place_code',
                'consolidtated_city_code',
                'name',
            ],
        )

        for row in reader:
            rows.append(row)

    return rows


def get_state_codes():
    dicts = get_census_dicts()

    states_by_code = {}
    states_by_name = {}
    for data in dicts:
        if data['summary_level'] == '040':  # states
            state_code = int(data['state_code'])
            name = data['name']
            states_by_code[state_code] = name
            states_by_name[name] = state_code

    return states_by_code, states_by_name


def get_county_codes():
    dicts = get_census_dicts()

    counties_by_int = {}
    counties_by_str = {}
    for data in dicts:
        if data['summary_level'] == '050':  # counties
            state_code = int(data['state_code'])
            county_code = int(data['county_code'])
            full_code_int = state_code * 1000 + county_code
            full_code_str = f'{full_code_int:05d}'
            name = data['name']

            county_data = {
                'name': name,
                'state_code': state_code,
                'county_code': county_code,
                'full_code_str': full_code_str,
                'full_code_int': full_code_int,
            }

            counties_by_int[full_code_int] = county_data
            counties_by_str[full_code_str] = county_data

    return counties_by_int, counties_by_str


def process_fips():
    features = read_json(fips_geojson_dir / 'counties_20m.geojson')['features']
    print(len(features))

    counties_by_str = get_county_codes()[1]

    write_json(data_dir / 'out.json', counties_by_str, indent=2, sort_keys=True)
    print(len(counties_by_str))

    states_by_code = get_state_codes()[0]

    for feature in features:
        prop = feature['properties']
        full_code_str = prop['GEOID']
        state_code = int(prop['STATEFP'])

        # skip minor islands without state code found in 500k dataset
        if state_code not in states_by_code:
            continue

        name_from_fips = counties_by_str[full_code_str]['name']
        countrylevel_id = f'fips:{full_code_str}'

        data = {
            'name': name_from_fips,
            'countrylevel_id': countrylevel_id,
            'fips': full_code_str,
            # 'population': population,
        }
