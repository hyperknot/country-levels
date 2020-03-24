import requests

from country_levels_lib.config import data_dir
from country_levels_lib.utils import write_json, read_json

wam_data_dir = data_dir / 'wam'


def make_config():
    pass


def write_empty_config():
    # file_path = wam_data_dir / 'codes.json'
    # if file_path.is_file():
    #     return read_json(file_path)

    countries = get_tree(0)

    codes = {}
    for c in countries:
        code = c['a_attr']['title'][:3]
        name = c['text'].split('(')[0].strip()
        codes[code] = {'name': name, 'levels': [2]}

    wam_data_dir.mkdir(parents=True, exist_ok=True)
    write_json(wam_data_dir / 'config_empty.json', codes, indent=2, sort_keys=True)
    return codes


def get_tree(id):
    cookies = {
        'some': 'cookie',
    }

    headers = {
        'User-Agent': 'country-levels (https://github.com/hyperknot/country-levels)',
        'Referer': 'https://wambachers-osm.website/boundaries/',
    }

    data = {
        'parent': str(id),
        #
        'addi': '4711',
        'database': 'planet3',
    }

    response = requests.post(
        'https://wambachers-osm.website/boundaries/getJsTree7',
        headers=headers,
        cookies=cookies,
        data=data,
    )

    response.raise_for_status()

    return response.json()
