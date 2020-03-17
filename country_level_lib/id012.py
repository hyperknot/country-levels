import re

from country_level_lib.config import geojson_dir, id_dir
from country_level_lib.utils import read_json, write_json


fix_iso_0_codes = {'FRA': 'FR', 'NOR': 'NO'}
iso_012_regex = re.compile('[A-Z]{2,3}')


def create_adm_iso_map(countries: list):
    """
    maps adm0_a3 values to iso_a2 where possible
    """
    adm_iso_map = {}
    for feature in countries:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        # country_name = prop['admin']
        iso = prop['iso_a2']
        if iso == '-99':
            # print(country_name, prop['iso_a2'], prop['adm0_a3'])
            iso = prop['adm0_a3']

        adm = prop['adm0_a3']
        if adm in adm_iso_map:
            raise ValueError(f'adm exists: {adm}')
        adm_iso_map[adm] = iso

    # manual fixing
    adm_iso_map = dict(adm_iso_map, **fix_iso_0_codes)

    return adm_iso_map


def process_id012():
    countries = read_json(geojson_dir / 'countries.geojson')['features']
    print(f'{len(countries)} countries')

    units = read_json(geojson_dir / 'units.geojson')['features']
    print(f'{len(units)} units')

    subunits = read_json(geojson_dir / 'subunits.geojson')['features']
    print(f'{len(subunits)} subunits')

    adm_iso_map = create_adm_iso_map(countries)
    levels = dict()

    for feature in countries:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        country_name = prop['admin']
        country_iso = adm_iso_map[prop['adm0_a3']]
        validate_iso_012(country_iso)

        ne_id = prop['ne_id']
        assert type(ne_id) == int

        id0 = f'id0:{country_iso}'

        levels.setdefault(id0, {'name': country_name, 'ne_id': ne_id, 'sub1': {}})

    for feature in units:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        country_iso = adm_iso_map[prop['adm0_a3']]
        validate_iso_012(country_iso)

        unit_name = prop['geounit']
        unit_iso = prop['gu_a3']
        validate_iso_012(unit_iso)

        ne_id = prop['ne_id']
        assert type(ne_id) == int

        id0 = f'id0:{country_iso}'
        id1 = f'id1:{unit_iso}'

        sub1 = levels[id0]['sub1']
        sub1.setdefault(id1, {'name': unit_name, 'ne_id': ne_id, 'sub2': {}})

    for feature in subunits:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        country_iso = adm_iso_map[prop['adm0_a3']]
        validate_iso_012(country_iso)

        unit_iso = prop['gu_a3']
        validate_iso_012(unit_iso)

        subunit_name = prop['subunit']
        subunit_iso = prop['su_a3']
        validate_iso_012(subunit_iso)

        ne_id = prop['ne_id']
        assert type(ne_id) == int

        id0 = f'id0:{country_iso}'
        id1 = f'id1:{unit_iso}'
        id2 = f'id2:{subunit_iso}'

        sub1 = levels[id0]['sub1']
        sub2 = sub1[id1]['sub2']
        sub2.setdefault(id2, {'name': subunit_name, 'ne_id': ne_id})

    # clean up sub2
    for sub_country, country_data in levels.items():
        for data1 in country_data['sub1'].values():
            if len(data1['sub2']) == 1:
                del data1['sub2']

    # clean up sub1
    for sub_country, country_data in levels.items():
        sub1 = country_data['sub1']

        if len(sub1) != 1:
            continue

        # we know there is only one element in the dict now
        sub1_first = list(sub1.values())[0]
        if 'sub2' not in sub1_first:
            del country_data['sub1']

    id_dir.mkdir(exist_ok=True, parents=True)
    write_json(id_dir / 'level_012.json', levels, indent=2, sort_keys=True)


def validate_iso_012(iso_code: str):
    if iso_012_regex.fullmatch(iso_code) is None:
        print(f'wrong level 1 code: {iso_code}')
