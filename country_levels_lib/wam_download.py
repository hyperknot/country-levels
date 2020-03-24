import shutil
import subprocess
import time

import requests

from country_levels_lib.config import data_dir, tmp_dir, geojson_dir
from country_levels_lib.utils import write_json, read_json

wam_data_dir = data_dir / 'wam'
wam_geojson_download_dir = geojson_dir / 'wam' / 'download'


def download_all_regions():
    config = read_json(wam_data_dir / 'config_empty.json')
    for country_code, country_data in config.items():
        print(country_data['name'])

        if country_code == 'USA':
            continue

        downloaded = download_country(country_code, 2, 8)
        if downloaded:
            time.sleep(10)

    download_country('USA', 2, 6)
    # needs manual downloading because USA is too big
    # download_country('USA', 7, 7, merge=True)
    # download_country('USA', 8, 8, merge=True)


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


def download_country(country_code, level_min=2, level_max=8, overwrite=False, merge=False):
    print(f'  Downloading {country_code} {level_min}-{level_max}')

    geojson_subdir = wam_geojson_download_dir / country_code
    if geojson_subdir.is_dir() and not (overwrite or merge):
        print('    skipping')
        return False

    params = (
        ('cliVersion', '1.0'),
        ('cliKey', '38acad66-1a9b-4dd3-9a9f-9b5883f3c295'),
        ('exportFormat', 'json'),
        ('exportLayout', 'levels'),
        ('exportAreas', 'land'),
        ('union', 'false'),
        ('selected', country_code),
        ('from_AL', str(level_min)),
        ('to_AL', str(level_max)),
    )

    response = requests.get(
        'https://wambachers-osm.website/boundaries/exportBoundaries', params=params, stream=True
    )

    response.raise_for_status()

    shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    zip_file_path = tmp_dir / f'{country_code}.zip'

    with open(zip_file_path, 'wb') as outfile:
        for block in response.iter_content(1024):
            outfile.write(block)

    if not merge:
        shutil.rmtree(geojson_subdir, ignore_errors=True)
    geojson_subdir.mkdir(parents=True, exist_ok=True)

    cmd = ['7z', 'x', f'-o{geojson_subdir}', str(zip_file_path)]
    p = subprocess.run(cmd, capture_output=True, text=True)

    if p.returncode != 0:
        print(f'Cmd was:\n{" ".join(cmd)}\n\nerror was:\n{p.stderr}')
        raise ValueError()

    print('    OK')
    return True
