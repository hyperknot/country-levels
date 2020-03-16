from pprint import pprint

from country_levels_lib.config import geojson_dir, level3_dir, tmp_dir, fixes_dir
from country_levels_lib.level0123 import create_adm_iso_map
from country_levels_lib.utils import read_json, write_json


def process_level_3():
    countries = read_json(geojson_dir / 'countries.geojson')['features']
    states = read_json(geojson_dir / 'states.geojson')['features']

    with (fixes_dir / 'duplicate_l3_ids.txt').open() as infile:
        duplicate_l3_ids = {l.strip() for l in infile.readlines()}

    print(f'{len(states)} states')

    adm_iso_map = create_adm_iso_map(countries)
    data = {}

    for feature in states:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        country_name = prop['admin']
        country_iso = adm_iso_map[prop['adm0_a3']]

        state_name = prop['name']
        state_iso = fix_l3_codes.get(prop['iso_3166_2'], prop['iso_3166_2'])

        # skipping unnamed places (tiny islands)
        if state_name is None:
            # print(state_iso)
            continue

        if state_iso.startswith('-99-'):
            # print(state_iso)
            continue

        # check if state's iso code matches country's iso code
        if state_iso.split('-')[0] != country_iso:
            print(repr(country_name), repr(state_name), repr(state_iso), repr(country_iso))

        data.setdefault(country_iso, {})

        # check duplicate iso codes
        # we need to add a unique id to each
        if state_iso in duplicate_l3_ids:
            state_iso = f'{state_iso}.{prop["ne_id"]}'
        if state_iso in data[country_iso]:
            print(f'duplicate state_iso: {state_iso}')

        data[country_iso][state_iso] = {'name': state_name}

    for country_iso, country_states in data.items():
        level3_dir.mkdir(exist_ok=True)
        filename = f'{country_iso.lower()}.json'
        write_json(level3_dir / filename, country_states, indent=2, sort_keys=True)
        # print(f'{filename} written')


fix_l3_codes = {
    'UA-43': 'RU-43',
    'UA-40': 'RU-40',
    'NL-SX': 'SX-01',
    'US-PR': 'PR-01',
    'TK-X01~': 'NZ-TK',
    'AU-X04~': 'ATC-01',
}
