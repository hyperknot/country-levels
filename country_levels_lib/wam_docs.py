from country_levels_lib.config import export_dir
from country_levels_lib.utils import read_json


def generate_iso1_list():
    iso1_json = read_json(export_dir / 'iso1.json')



    print(iso1_json)
