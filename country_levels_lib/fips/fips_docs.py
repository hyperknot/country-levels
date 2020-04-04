from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.fips.fips_utils import get_state_data
from country_levels_lib.utils import read_json, write_file


def generate_fips_list():
    fips_json = read_json(export_dir / 'fips.json')
    counties = sorted(fips_json.values(), key=lambda k: k['name'])
    states_by_int = get_state_data()[0]

    doc_md = f'# US county FIPS code list\n'
    doc_md += '[GeoJSON for all counties](../export/geojson/q5/fips_all.geojson)'

    county_by_state = {}
    for item in sorted(counties, key=lambda k: k['state_code_int']):
        state_code_int = item['state_code_int']
        county_by_state.setdefault(state_code_int, [])
        county_by_state[state_code_int].append(item)

    for state_code_int, state_items in county_by_state.items():
        state_name = states_by_int[state_code_int]['name']
        state_code_postal = states_by_int[state_code_int]['postal_code']
        doc_md += f'\n\n#### {state_name} - {state_code_postal}, state code: {state_code_int}\n'
        doc_md += 'Name | FIPS | GeoJSON | population \n'
        doc_md += '--- | --- | --- | --: \n'

        for item in sorted(state_items, key=lambda k: k['name']):
            fips = item['fips']
            name_long = item['name_long']
            population = item['population']
            geojson_path = item['geojson_path']

            population_str = ''
            if population:
                population_str = f'{population:,}'

            geojson_link = f'[GeoJSON](../export/geojson/q8/{geojson_path})'

            doc_md += f'{name_long} | {fips} | {geojson_link} | {population_str}\n'

    write_file(docs_dir / 'fips_list.md', doc_md)
