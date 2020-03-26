import csv

from country_levels_lib.config import data_dir, geojson_dir
from country_levels_lib.utils import read_json
from country_levels_lib.wam_download import wam_geojson_download_dir

fips_data_dir = data_dir / 'fips'
census_csv = fips_data_dir / 'census.csv'
census_geojson_dir = geojson_dir / 'census'


def collect_fips():
    collect_from_osm()


def get_census_dicts():
    rows = list()

    with open(census_csv, newline='') as csvfile:
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


def collect_from_osm():
    features = read_json(census_geojson_dir / 'counties_20m.geojson')['features']
    print(len(features))

    counties_by_str = get_county_codes()[1]
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

        new_prop = {'name': '1'}
