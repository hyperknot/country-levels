import csv

from country_levels_lib.fips_process import fips_data_dir


def get_census_dicts():
    rows = list()

    with open(fips_data_dir / 'fips.csv', newline='') as csvfile:
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
        # states
        if data['summary_level'] != '040':
            continue

        state_code = int(data['state_code'])
        name = data['name']
        states_by_code[state_code] = name
        states_by_name[name] = state_code

    return states_by_code, states_by_name


def get_county_data():
    dicts = get_census_dicts()

    population_data = get_population_data()

    counties_by_int = {}
    counties_by_str = {}
    for data in dicts:
        # counties
        if data['summary_level'] != '050':
            continue

        state_code = int(data['state_code'])
        county_code = int(data['county_code'])
        full_code_int = state_code * 1000 + county_code
        full_code_str = f'{full_code_int:05d}'
        name = data['name']

        population = population_data.get(full_code_str)

        county_data = {
            'name': name,
            'state_code': state_code,
            'county_code': county_code,
            'full_code_str': full_code_str,
            'full_code_int': full_code_int,
            'population': population,
        }

        counties_by_int[full_code_int] = county_data
        counties_by_str[full_code_str] = county_data

    return counties_by_int, counties_by_str


def get_population_data():
    counties_by_str = {}

    with open(fips_data_dir / 'population.csv', newline='', errors='surrogateescape') as csvfile:
        reader = csv.DictReader(csvfile,)

        for row in reader:
            if row['SUMLEV'] != '050':
                continue

            state_code = int(row['STATE'])
            county_code = int(row['COUNTY'])
            full_code_int = state_code * 1000 + county_code
            full_code_str = f'{full_code_int:05d}'

            population = int(row['POPESTIMATE2019'])
            counties_by_str[full_code_str] = population

    return counties_by_str
