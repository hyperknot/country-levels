import csv

from country_levels_lib.config import data_dir

fips_data_dir = data_dir / 'fips'


def get_state_data():
    state_postal_codes = get_state_postal_codes()
    all_geocode_data = get_all_geocode_data()

    states_by_int = {}
    states_by_postal = {}
    for geocode_row in all_geocode_data:
        # states
        if geocode_row['summary_level'] != '040':
            continue

        state_int_code = int(geocode_row['state_code'])
        state_postal_code = state_postal_codes[state_int_code]
        name = geocode_row['name']

        state_data = {
            'name': name,
            'int_code': state_int_code,
            'postal_code': state_postal_code,
        }

        states_by_int[state_int_code] = state_data
        states_by_postal[state_postal_code] = state_data

    return states_by_int, states_by_postal


def get_county_data():
    all_geocode_data = get_all_geocode_data()
    population_data = get_population_data()
    states_by_int = get_state_data()[0]

    counties_by_int = {}
    counties_by_str = {}
    for data in all_geocode_data:
        # counties
        if data['summary_level'] != '050':
            continue

        state_code_int = int(data['state_code'])
        state_code_postal = states_by_int[state_code_int]['postal_code']
        state_code_iso = f'US-{state_code_postal}'
        county_code = int(data['county_code'])
        full_code_int = state_code_int * 1000 + county_code
        full_code_str = f'{full_code_int:05d}'

        name = data['name']
        name_long = f'{name}, {state_code_postal}'

        population = population_data.get(full_code_str)

        county_data = {
            'name': name,
            'name_long': name_long,
            'state_code_int': state_code_int,
            'state_code_postal': state_code_postal,
            'state_code_iso': state_code_iso,
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


def get_all_geocode_data():
    rows = list()

    with open(fips_data_dir / 'all-geocodes.csv', newline='') as csvfile:
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
            row['name'] = row['name'].replace('city', 'City')
            rows.append(row)

    return rows


def get_state_postal_codes():
    states_by_code = dict()

    with open(fips_data_dir / 'state_postal_codes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        for row in reader:
            state_code = int(row['STATE'])
            postal_code = row['STUSAB']
            states_by_code[state_code] = postal_code

    return states_by_code
