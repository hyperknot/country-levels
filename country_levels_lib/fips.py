import csv
from itertools import islice

from country_levels_lib.config import data_dir

fips_data_dir = data_dir / 'fips'
census_csv = fips_data_dir / 'census.csv'


def collect_fips():
    state_codes = get_state_codes()


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
        if data['summary_level'] == '040':
            state_code = int(data['state_code'])
            name = data['name']
            states_by_code[state_code] = name
            states_by_name[name] = state_code

    return states_by_code, states_by_name
