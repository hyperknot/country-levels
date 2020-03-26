from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.utils import read_json, write_file, osm_url, wikidata_url, wikipedia_url


def generate_iso1_list():
    iso1_json = read_json(export_dir / 'iso1.json')

    doc_md = (
        '# ISO 3166-1 list\n'
        'Name | ISO code | GeoJSON | ISO 2 | OSM | Wikidata | Wikipedia | population \n'
        '--- | --- | --- | --- | --- | --- | --- | --- \n'
    )

    for item in sorted(iso1_json.values(), key=lambda k: k['name']):
        data = build_row_data(item)

        iso1 = item['iso1']
        geojson_link = f'[GeoJSON](../export/geojson/q7/iso1/{iso1.upper()}.geojson)'

        iso_2_link = ''

        doc_md += (
            f'{data["name"]} | {iso1} | {geojson_link} | {iso_2_link} | '
            f'{data["osm_link"]} | {data["wikidata_link"]} | '
            f'{data["wikipedia_link"]} | {data["population"]}'
            f'\n'
        )

    write_file(docs_dir / 'iso1_list.md', doc_md)


def build_row_data(item):
    name = item['name']
    osm_id = item['osm_id']
    countrylevel_id = item['countrylevel_id']
    population = item['population']

    wikidata_id = item.get('wikidata_id')
    wikipedia_id = item.get('wikipedia_id')

    osm_link = f'[OSM]({osm_url(osm_id)})'

    wikidata_link = ''
    if wikidata_id:
        wikidata_link = f'[Wikidata]({wikidata_url(wikidata_id)})'

    wikipedia_link = ''
    if wikipedia_id:
        wikipedia_link = f'[Wikipedia]({wikipedia_url(wikipedia_id)})'

    return {
        'name': name,
        'osm_link': osm_link,
        'countrylevel_id': countrylevel_id,
        'population': population,
        'wikidata_link': wikidata_link,
        'wikipedia_link': wikipedia_link,
    }
