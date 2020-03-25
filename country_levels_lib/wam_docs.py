from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.utils import read_json, write_file, osm_url, wikidata_url, wikipedia_url


def generate_iso1_list():
    iso1_json = read_json(export_dir / 'iso1.json')

    doc_md = (
        '# ISO 3166-1 list\n'
        'Name | ISO code | GeoJSON | ISO 2 | OSM | Wikidata | Wikipedia | population \n'
        '--- | --- | --- | --- | --- | --- | --- | --- \n'
    )

    for feature in iso1_json.values():
        name = feature['name']
        iso1 = feature['iso1']
        osm_id = feature['osm_id']
        countrylevel_id = feature['countrylevel_id']
        population = feature['population']

        wikidata_id = feature.get('wikidata_id')
        wikipedia_id = feature.get('wikipedia_id')

        osm_link = f'[OSM]({osm_url(osm_id)})'

        wikidata_link = ''
        if wikidata_id:
            wikidata_link = f'[Wikidata]({wikidata_url(wikidata_id)})'

        wikipedia_link = ''
        if wikipedia_id:
            wikipedia_link = f'[Wikipedia]({wikipedia_url(wikipedia_id)})'

        iso_2_link = ''

        doc_md += (
            f'{name} | {iso1} | GeoJSON | {iso_2_link} | '
            f'{osm_link} | {wikidata_link} | '
            f'{wikipedia_link} | {population}'
            f'\n'
        )

    write_file(docs_dir / 'iso1_list.md', doc_md)
