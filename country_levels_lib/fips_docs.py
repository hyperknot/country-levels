from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.utils import read_json, write_file


def generate_fips_list():
    fips_json = read_json(export_dir / 'fips.json')
    counties = sorted(fips_json.values(), key=lambda k: k['name'])

    doc_md = f'# US County FIPS list\n'

    county_by_state = {}
    for item in sorted(counties, key=lambda k: k['state_code']):
        state_code = item['state_code']
        county_by_state.setdefault(state_code, [])
        county_by_state[state_code].append(item)

    for state_code, state_items in county_by_state.items():
        doc_md += f'\n\n#### State {state_code}\n'
        doc_md += 'Name | FIPS | GeoJSON | population \n'
        doc_md += '--- | --- | --- | --: \n'

        for item in sorted(state_items, key=lambda k: k['name']):
            fips = item['fips']
            name = item['name']
            population = item['population']

            population_str = ''
            if population:
                population_str = f'{population:,}'

            state_code_str = fips[:2]
            geojson_link = f'[GeoJSON](../export/geojson/q7/fips/{state_code_str}/{fips}.geojson)'

            doc_md += f'{name} | {fips} | {geojson_link} | {population_str}\n'

    write_file(docs_dir / 'fips_list.md', doc_md)
