from country_levels_lib.utils import read_json


def process_level_012():
    countries = read_json(countries_dir / 'geojson' / 'countries.geojson')['features']
    print(f'{len(countries)} countries')

    units = read_json(countries_dir / 'geojson' / 'units.geojson')['features']
    print(f'{len(units)} units')

    subunits = read_json(countries_dir / 'geojson' / 'subunits.geojson')['features']
    print(f'{len(subunits)} subunits')
