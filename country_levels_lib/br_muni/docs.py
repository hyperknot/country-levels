from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.utils import read_json, write_file


def generate_br_muni_list():
    br_muni_json = read_json(export_dir / 'br_muni.json')
    counties = sorted(br_muni_json.values(), key=lambda k: k['name'])

    doc_md = f'# Brazil municipality IBGE code list\n'
    doc_md += '[GeoJSON for all municipalities](../export/geojson/q5/br_muni_all.geojson)'

    county_by_state = {}
    for item in sorted(counties, key=lambda k: k['state_code']):
        state_code = item['state_code']
        county_by_state.setdefault(state_code, [])
        county_by_state[state_code].append(item)

    for state_code, state_items in county_by_state.items():
        doc_md += f'\n\n#### {state_code}\n'
        doc_md += 'Name | IBGE code | GeoJSON | population \n'
        doc_md += '--- | --- | --- | --: \n'

        for item in sorted(state_items, key=lambda k: k['name']):
            ibge_code = item['ibge_code']
            name_long = item['name_long']
            population = item['population']
            geojson_path = item['geojson_path']

            population_str = ''
            if population:
                population_str = f'{population:,}'

            geojson_link = f'[GeoJSON](../export/geojson/q8/{geojson_path})'

            doc_md += f'{name_long} | {ibge_code} | {geojson_link} | {population_str}\n'

    write_file(docs_dir / 'br_muni_list.md', doc_md)
